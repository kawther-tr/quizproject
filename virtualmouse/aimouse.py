import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

# --- Config ---
wCam, hCam = 640, 480
frameR     = 100   # marge de réduction du cadre
smoothening = 7    # lissage du mouvement

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
prev_state   = None   # pour n'afficher le state que quand il change

while True:
    success, img = cap.read()

    # 1. Détection de la main
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:

        # 2. Lire l'état des 5 doigts
        fingers = detector.fingersUp()
        # fingers[0]=pouce, [1]=index, [2]=majeur, [3]=annulaire, [4]=auriculaire
        total = sum(fingers)

        # ── MODE DÉPLACEMENT : paume ouverte (5 doigts levés) ──────────────
        if total == 5:
            # Coordonnées du centre de la main (landmark 9 = milieu de la paume)
            cx, cy = lmList[9][1], lmList[9][2]

            # Convertir coordonnées caméra → coordonnées écran
            x3 = np.interp(cx, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(cy, (frameR, hCam - frameR), (0, hScr))

            # Lissage exponentiel
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY

            # Affichage console (une seule fois par changement d'état)
            if prev_state != "MOVE":
                print("[SOURIS] Etat : DEPLACEMENT")
                prev_state = "MOVE"

            cv2.putText(img, "MODE : DEPLACEMENT", (20, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # ── MODE CLIC : poing fermé (0 doigt levé) ─────────────────────────
        elif total == 0:
            autopy.mouse.click()
            time.sleep(0.3)   # anti-rebond pour éviter les double-clics

            if prev_state != "CLICK":
                print("[SOURIS] Etat : CLIC")
                prev_state = "CLICK"

            cv2.putText(img, "MODE : CLIC", (20, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 100, 255), 2)

        # ── GESTE NON RECONNU ───────────────────────────────────────────────
        else:
            if prev_state != "IDLE":
                print("[SOURIS] Etat : EN ATTENTE")
                prev_state = "IDLE"

            cv2.putText(img, "EN ATTENTE", (20, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 2)

    # 3. Affichage FPS
    cTime = time.time()
    fps   = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 90),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 2)

    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) == 27:   # ESC pour quitter
        break

cap.release()
cv2.destroyAllWindows()
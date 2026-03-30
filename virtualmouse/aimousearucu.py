import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import HandTrackingModule as htm
import autopy
import time

# ================= CONFIG =================
wCam, hCam = 480, 360
frameR = 100
smoothening = 2
TARGET_ID = 0

# ================= INIT =================
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

plocX, plocY = 0, 0
prev_state = None
pTime = 0

# ================= YOLO =================
model = YOLO("yolov8n-seg.pt")

# ================= MEDIAPIPE =================
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# ================= ARUCO =================
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()

# ================= VARIABLES =================
player_selected = False
selected_bbox = None
iou_threshold = 0.3
frames_lost = 0

# ================= IOU =================
def compute_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])

    return interArea / float(boxAArea + boxBArea - interArea)
frame_count = 0
results = None
# ================= LOOP =================
while True:
    success, img = cap.read()
    if not success:
        break

    h, w = img.shape[:2]

    # ===== YOLO DETECTION =====
    frame_count += 1

    if frame_count % 3 == 0:
        results = model(img, verbose=False)[0]
   
    if results is None:
       continue
    bboxes = []
    if results is not None and results.boxes is not None:
        for box in results.boxes.data:
            if int(box[5]) == 0:  # personne
                x1, y1, x2, y2 = map(int, box[:4])
                bboxes.append((x1, y1, x2, y2))

    # ===== ARUCO =====
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    # ===== SELECTION JOUEUR =====
    if not player_selected and ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id == TARGET_ID:

                pts = corners[i][0]
                cx = int(np.mean(pts[:, 0]))
                cy = int(np.mean(pts[:, 1]))

                for bbox in bboxes:
                    if bbox[0] < cx < bbox[2] and bbox[1] < cy < bbox[3]:
                        selected_bbox = bbox
                        player_selected = True
                        frames_lost = 0
                        print("✅ Joueur sélectionné")
                        break

    # ===== TRACKING IOU =====
    matched = False
    if player_selected and selected_bbox:
        for bbox in bboxes:
            if compute_iou(selected_bbox, bbox) > iou_threshold:
                selected_bbox = bbox
                matched = True
                break

        if not matched:
            frames_lost += 1
            if frames_lost > 10:
                print("❌ Joueur perdu")
                player_selected = False
                selected_bbox = None

    # ===== HAND TRACKING =====
    img = detector.findHands(img,draw=False)
    lmList, _ = detector.findPosition(img)

    if player_selected and selected_bbox:
        x1, y1, x2, y2 = selected_bbox
        margin = 300  # 🔥 ajuste entre 50 et 150

        x1e = max(0, x1 - margin)
        y1e = max(0, y1 - margin)
        x2e = min(w, x2 + margin)
        y2e = min(h, y2 + margin)
        # dessiner bbox joueur
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if len(lmList) != 0:
            hx, hy = lmList[9][1], lmList[9][2]

            # 🔥 NOUVELLE LOGIQUE (ANTI-TRICHE)
            # main doit être DANS le bbox joueur
            #if x1 < hx < x2 and y1 < hy < y2:
            if x1e < hx < x2e and y1e < hy < y2e:
                fingers = detector.fingersUp()
                total = sum(fingers)

                # ===== MOVE =====
                if total == 5:
                    speed_factor = 1.5  # 🔥 augmente la vitesse

                    x3 = np.interp(hx, (frameR, wCam - frameR), (0, wScr)) * speed_factor
                    y3 = np.interp(hy, (frameR, hCam - frameR), (0, hScr)) * speed_factor

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    
                    margin = 5
                    clocX = max(margin, min(wScr - margin, clocX))
                    clocY = max(margin, min(hScr - margin, clocY))
                   
                    autopy.mouse.move(wScr - clocX, clocY)
                    plocX, plocY = clocX, clocY

                    cv2.putText(img, "MOVE", (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

                # ===== CLICK =====
                elif total == 0:
                    autopy.mouse.click()
                    time.sleep(0.3)

                    cv2.putText(img, "CLICK", (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                else:
                    cv2.putText(img, "IDLE", (20, 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 200), 2)

                cv2.circle(img, (hx, hy), 10, (0, 255, 0), -1)

            else:
                cv2.putText(img, "MAIN HORS JOUEUR", (20, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    else:
        cv2.putText(img, "RECHERCHE JOUEUR (ARUCO)", (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    # ===== FPS =====
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (20, 90),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 2)

    cv2.imshow("Fusion YOLO + ArUco + Hand", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
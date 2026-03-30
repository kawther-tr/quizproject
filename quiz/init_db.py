import sqlite3

conn = sqlite3.connect('quiz.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        theme    TEXT NOT NULL,
        question TEXT NOT NULL,
        choices  TEXT NOT NULL,
        answer   TEXT NOT NULL
    )
''')

questions = [
    # ── Maths ──
    ("math", "Combien font 5 × 3 ?", "15|10|20|8", "15"),
    ("math", "Combien font 9 × 6 ?", "54|56|49|64", "54"),
    ("math", "Combien font 15 + 27 ?", "42|40|43|41", "42"),
    ("math", "Combien font 7 × 8 ?", "54|56|58|60", "56"),
    ("math", "Combien de côtés a un hexagone ?", "5|6|7|8", "6"),
    ("math","Combien font 12 × 4 ?","48|46|52|44","48"),
    ("math","Combien font 100 ÷ 5 ?","20|25|15|30","20"),
    ("math","Combien font 9² ?","81|72|90|99","81"),
    ("math","Combien font 50 - 18 ?","32|30|28|35","32"),
    ("math","Combien font 7³ ?","343|240|300|350","343"),
    ("math","Combien font 6 × 11 ?","66|60|72|68","66"),
    ("math","Combien font 144 ÷ 12 ?","12|10|14|16","12"),
    ("math","Combien font 25 × 4 ?","100|90|80|110","100"),
    ("math","Combien font 81 ÷ 9 ?","9|8|7|6","9"),
    ("math","Combien font 13 + 29 ?","42|40|41|43","42"),
    ("math","Combien font 2⁵ ?","32|16|64|24","32"),
    ("math","Combien font 90 ÷ 3 ?","30|25|20|35","30"),
    ("math","Combien font 18 × 2 ?","36|34|38|40","36"),
    ("math","Combien font 49 ÷ 7 ?","7|6|8|9","7"),
    ("math","Combien font 11 × 11 ?","121|111|131|101","121"),
    ("math","Combien font 64 ÷ 8 ?","8|7|6|9","8"),
    ("math","Combien font 20² ?","400|200|300|500","400"),
    ("math","Combien font 17 + 26 ?","43|42|41|44","43"),
    ("math","Combien font 15 × 5 ?","75|70|80|85","75"),
    ("math","Combien font 72 ÷ 6 ?","12|10|14|16","12"),

    # ── Culture générale ──
    ("culture", "Quelle est la capitale de la Tunisie ?", "Tunis|Sfax|Sousse|Nabeul", "Tunis"),
    ("culture", "Quelle est la capitale de l'Allemagne ?", "Berlin|Madrid|Vienne|Prague", "Berlin"),
    ("culture", "Qui a peint la Joconde ?", "Van Gogh|Picasso|Léonard de Vinci|Monet", "Léonard de Vinci"),
    ("culture", "Quelle langue est parlée au Brésil ?", "Espagnol|Portugais|Français|Anglais", "Portugais"),
    ("culture", "Combien de continents y a-t-il ?", "5|6|7|8", "7"),
    ("culture","Quelle est la capitale de l’Italie ?","Rome|Milan|Naples|Turin","Rome"),
    ("culture","Quel pays a pour capitale Tokyo ?","Japon|Chine|Corée|Thaïlande","Japon"),
    ("culture","Qui a écrit 'Hamlet' ?","Shakespeare|Molière|Hugo|Balzac","Shakespeare"),
    ("culture","Quelle est la plus grande planète ?","Jupiter|Mars|Terre|Saturne","Jupiter"),
    ("culture","Quel océan borde l’Afrique à l’ouest ?","Atlantique|Pacifique|Indien|Arctique","Atlantique"),
    ("culture","Quelle est la monnaie de l’Europe ?","Euro|Dollar|Livre|Yen","Euro"),
    ("culture","Qui a découvert l’Amérique ?","Christophe Colomb|Magellan|Cook|Vespucci","Christophe Colomb"),
    ("culture","Quelle est la langue officielle en Espagne ?","Espagnol|Français|Italien|Portugais","Espagnol"),
    ("culture","Quel désert est le plus grand ?","Sahara|Gobi|Kalahari|Arctique","Sahara"),
    ("culture","Quel pays a une feuille d’érable sur son drapeau ?","Canada|USA|Australie|Suède","Canada"),
    ("culture","Quelle est la capitale du Maroc ?","Rabat|Casablanca|Marrakech|Fès","Rabat"),
    ("culture","Combien de jours dans une semaine ?","7|5|6|8","7"),
    ("culture","Quel est le plus long fleuve d’Europe ?","Volga|Danube|Seine|Rhin","Volga"),
    ("culture","Quel pays est connu pour les pyramides ?","Égypte|Mexique|Pérou|Inde","Égypte"),
    ("culture","Quelle mer sépare l’Europe et l’Afrique ?","Méditerranée|Rouge|Noire|Baltique","Méditerranée"),
    ("culture","Quelle est la capitale de la France ?","Paris|Lyon|Marseille|Nice","Paris"),
    ("culture","Qui a peint 'La Nuit étoilée' ?","Van Gogh|Monet|Picasso|Da Vinci","Van Gogh"),
    ("culture","Quel est le plus petit pays du monde ?","Vatican|Monaco|Malte|Luxembourg","Vatican"),
    ("culture","Quelle langue parle-t-on en Allemagne ?","Allemand|Anglais|Français|Italien","Allemand"),
    ("culture","Quel est le symbole de la paix ?","Colombe|Lion|Aigle|Serpent","Colombe"),

    # ── Science ──
    ("science", "Quel est le plus grand océan ?", "Atlantique|Indien|Pacifique|Arctique", "Pacifique"),
    ("science", "Quel gaz respirons-nous principalement ?", "Oxygène|Azote|CO2|Hydrogène", "Azote"),
    ("science", "Quel est le plus long fleuve du monde ?", "Nil|Amazone|Yangtsé|Mississippi", "Amazone"),
    ("science", "Quel est l'animal le plus rapide sur terre ?", "Lion|Guépard|Cheval|Tigre", "Guépard"),
    ("science", "Quel continent est le plus grand ?", "Afrique|Europe|Asie|Amérique", "Asie"),
    ("science","Quelle planète est la plus proche du Soleil ?","Mercure|Vénus|Mars|Terre","Mercure"),
    ("science","Quel organe pompe le sang ?","Cœur|Poumon|Foie|Rein","Cœur"),
    ("science","Quel est l’état de l’eau à 0°C ?","Solide|Liquide|Gaz|Plasma","Solide"),
    ("science","Quel gaz est nécessaire à la respiration ?","Oxygène|CO2|Azote|Hydrogène","Oxygène"),
    ("science","Quel est le satellite de la Terre ?","Lune|Mars|Soleil|Vénus","Lune"),
    ("science","Quelle planète est rouge ?","Mars|Jupiter|Saturne|Neptune","Mars"),
    ("science","Quel est le centre du système solaire ?","Soleil|Terre|Mars|Lune","Soleil"),
    ("science","Quel est l’état du soleil ?","Plasma|Liquide|Solide|Gaz","Plasma"),
    ("science","Quelle force nous attire vers le sol ?","Gravité|Magnétisme|Électricité|Pression","Gravité"),
    ("science","Quel est le plus grand organe du corps ?","Peau|Cœur|Foie|Cerveau","Peau"),
    ("science","Quel est le point d’ébullition de l’eau ?","100°C|90°C|80°C|70°C","100°C"),
    ("science","Quel est le symbole de la Terre ?","🌍|🔥|💧|🌪","🌍"),
    ("science","Combien de planètes dans le système solaire ?","8|7|9|10","8"),
    ("science","Quel organe permet de respirer ?","Poumons|Cœur|Foie|Rein","Poumons"),
    ("science","Quel est le plus petit os du corps ?","Étrier|Fémur|Tibia|Radius","Étrier"),
    ("science","Quelle planète a des anneaux ?","Saturne|Mars|Vénus|Mercure","Saturne"),
    ("science","Quelle est la vitesse de la lumière ?","300000 km/s|150000|100000|50000","300000 km/s"),
    ("science","Quel est le principal gaz de l’air ?","Azote|Oxygène|CO2|Hydrogène","Azote"),
    ("science","Quelle planète est la plus grande ?","Jupiter|Mars|Terre|Saturne","Jupiter"),
    ("science","Quel organe contrôle le corps ?","Cerveau|Cœur|Foie|Poumon","Cerveau"),


    # ── Chimie ──
    ("chimie", "Quel est le symbole chimique de l'eau ?", "O2|CO2|H2O|HO", "H2O"),
    ("chimie", "Quel est le symbole du fer ?", "Fe|Fr|Fo|Fi", "Fe"),
    ("chimie", "Quel gaz est produit par la photosynthèse ?", "CO2|O2|N2|H2", "O2"),
    ("chimie", "Quel est le numéro atomique de l'hydrogène ?", "1|2|3|4", "1"),
    ("chimie", "Quelle est la formule du sel de cuisine ?", "NaCl|KCl|CaCl|MgCl", "NaCl"),
    ("chimie","Quel est le symbole de l’oxygène ?","O|O2|Ox|Og","O"),
    ("chimie","Quel est le symbole du carbone ?","C|Ca|Co|Cr","C"),
    ("chimie","Quel est le symbole de l’or ?","Au|Ag|Fe|Go","Au"),
    ("chimie","Quel est le pH de l’eau pure ?","7|6|8|5","7"),
    ("chimie","Quel est le symbole du sodium ?","Na|So|Sn|Sd","Na"),
    ("chimie","Quel est le symbole du potassium ?","K|P|Po|Pt","K"),
    ("chimie","Quel gaz est CO2 ?","Dioxyde de carbone|Oxygène|Azote|Hydrogène","Dioxyde de carbone"),
    ("chimie","Quel est le symbole du calcium ?","Ca|Cl|C|Cm","Ca"),
    ("chimie","Quel est le symbole du chlore ?","Cl|C|Ch|Cr","Cl"),
    ("chimie","Quel est le symbole de l’argent ?","Ag|Au|Ar|An","Ag"),
    ("chimie","Quel est le symbole du zinc ?","Zn|Z|Zi|Zc","Zn"),
    ("chimie","Quel est le symbole du cuivre ?","Cu|Co|Cr|C","Cu"),
    ("chimie","Quel est le symbole de l’hélium ?","He|H|Ho|Hu","He"),
    ("chimie","Quel est le symbole de l’azote ?","N|Na|Ne|No","N"),
    ("chimie","Quel est le symbole du phosphore ?","P|Ph|Po|Pa","P"),
    ("chimie","Quel est le symbole du soufre ?","S|So|Su|Sf","S"),
    ("chimie","Quel est le symbole du plomb ?","Pb|Pl|Pm|Po","Pb"),
    ("chimie","Quel est le symbole du magnésium ?","Mg|Mn|Me|Ma","Mg"),
    ("chimie","Quel est le symbole du fluor ?","F|Fl|Fr|Fo","F"),
    ("chimie","Quel est le symbole du nickel ?","Ni|Ne|Na|No","Ni"),
]

conn.executemany(
    "INSERT INTO questions (theme, question, choices, answer) VALUES (?,?,?,?)",
    questions
)
conn.commit()
conn.close()
print("Base de données créée avec succès !")
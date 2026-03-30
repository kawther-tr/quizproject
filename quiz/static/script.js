let questions = [];
let index = 0;
let score = 0;

// ── Au démarrage : charger les thèmes ──
fetch('/themes')
    .then(res => res.json())
    .then(themes => showThemes(themes));

// Icônes pour chaque thème
const icones = {
    "math":    "🧮",
    "culture": "🌍",
    "science": "🔬",
    "chimie":  "⚗️",
};

function showThemes(themes) {
    const list = document.getElementById("theme-list");
    list.innerHTML = "";

    themes.forEach((theme, i) => {
        let btn = document.createElement("button");
        btn.classList.add("theme-btn");
        btn.innerHTML = `${icones[theme] || "📚"} ${theme.charAt(0).toUpperCase() + theme.slice(1)}`;
        
        // Animation décalée pour chaque bouton
        btn.style.opacity = "0";
        btn.style.transform = "translateY(20px)";
        btn.style.transition = `all 0.4s cubic-bezier(0.4,0,0.2,1) ${i * 0.1}s`;

        btn.onclick = () => startQuiz(theme);
        list.appendChild(btn);

        // Déclencher l'animation après insertion
        setTimeout(() => {
            btn.style.opacity = "1";
            btn.style.transform = "translateY(0)";
        }, 50);
    });
}

function startQuiz(theme) {
    // Cacher l'écran thème, montrer le quiz
    document.getElementById("theme-screen").style.display = "none";
    document.getElementById("quiz").style.display = "block";

    // Charger 20 questions aléatoires du thème choisi
    fetch(`/questions/${theme}`)
        .then(res => res.json())
        .then(data => {
            questions = data;
            index = 0;
            score = 0;
            showQuestion();
        });
}

function showQuestion() {
    let q = questions[index];

    document.getElementById("q-num").innerText = `Question ${index + 1} / ${questions.length}`;
    document.getElementById("progress").style.width = (index / questions.length * 100) + "%";
    document.getElementById("score-badge").innerText = `Score : ${score}`;

    const quiz = document.getElementById("quiz");
    quiz.style.animation = "none";
    void quiz.offsetWidth;
    quiz.style.animation = "slide-in 0.4s cubic-bezier(0.4,0,0.2,1) forwards";

    document.getElementById("question").innerText = q.question;

    let answersDiv = document.getElementById("answers");
    answersDiv.innerHTML = "";

    q.choices.forEach(choice => {
        let btn = document.createElement("button");
        btn.innerText = choice;

        btn.onclick = () => {
            answersDiv.querySelectorAll("button").forEach(b => b.classList.add("disabled"));

            if (choice === q.answer) {
                score++;
                btn.classList.add("correct");
                showToast("✅ Correct !", "correct");
            } else {
                btn.classList.add("wrong");
                answersDiv.querySelectorAll("button").forEach(b => {
                    if (b.innerText === q.answer) b.classList.add("correct");
                });
                showToast("❌ Faux !", "wrong");
            }

            setTimeout(() => {
                index++;
                if (index < questions.length) {
                    showQuestion();
                } else {
                    showResult();
                }
            }, 1400);
        };

        answersDiv.appendChild(btn);
    });
}

function showResult() {
    document.getElementById("progress").style.width = "100%";

    const pct = score / questions.length;
    let emoji = "😅", msg = "Continuez à apprendre !";
    if (pct >= 0.9) { emoji = "🏆"; msg = "Excellent ! Vous êtes un champion !"; }
    else if (pct >= 0.7) { emoji = "🎉"; msg = "Très bien ! Beau travail !"; }
    else if (pct >= 0.5) { emoji = "👍"; msg = "Pas mal, vous pouvez faire mieux !"; }

    document.getElementById("quiz").innerHTML = `
        <div id="result-box">
            <span class="emoji">${emoji}</span>
            <h2>Quiz terminé !</h2>
            <p>${msg}</p>
            <div class="final-score">${score} / ${questions.length}</div><br>
            <button id="restart-btn" onclick="backToThemes()">🔄 Choisir un autre thème</button>
        </div>
    `;
}

function backToThemes() {
    document.getElementById("quiz").style.display = "none";
    document.getElementById("quiz").innerHTML = `
        <p id="q-num">Question 1 / 20</p>
        <h1 id="question">Chargement...</h1>
        <div id="answers"></div>
    `;
    document.getElementById("progress").style.width = "0%";
    document.getElementById("score-badge").innerText = "Score : 0";
    document.getElementById("theme-screen").style.display = "block";
}

function showToast(message, type) {
    let toast = document.getElementById("toast");
    toast.innerText = message;
    toast.className = "show " + type;
    setTimeout(() => { toast.className = ""; }, 1400);
}

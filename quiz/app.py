from flask import Flask, render_template, jsonify, request
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route principale
@app.route("/")
def index():
    return render_template("index.html")

# Retourne la liste des thèmes disponibles
@app.route("/themes")
def get_themes():
    conn = get_db()
    themes = conn.execute("SELECT DISTINCT theme FROM questions").fetchall()
    conn.close()
    return jsonify([t["theme"] for t in themes])

# Retourne 20 questions aléatoires pour un thème
@app.route("/questions/<theme>")
def get_questions(theme):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM questions WHERE theme = ? ORDER BY RANDOM() LIMIT 20",
        (theme,)
    ).fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({
            "question": row["question"],
            "choices": row["choices"].split("|"),  # séparateur entre les choix
            "answer": row["answer"]
        })
    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
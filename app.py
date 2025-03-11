from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_answers():
    with open("answers.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
# Загружаем задания из JSON
def load_practical_tasks():
    with open("practical_tasks.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()
    if request.method == 'POST':
        score = 0
        total = len(questions)
        answers = load_answers()
        unanswered = []
        user_answers = {}
        
        for question in questions:
            user_answer = request.form.get(question['question'])
            if not user_answer:
                unanswered.append(question['question'])
            else:
                user_answers[question['question']] = user_answer
                if user_answer == answers[question['question']]:
                    score += 1
        
        if unanswered:
            return render_template('quiz.html', questions=questions, unanswered=unanswered, message="Вы не ответили на некоторые вопросы", user_answers=user_answers)
        
        percentage = (score / total) * 100
        return render_template('result.html', score=score, total=total, percentage=percentage)
    
    return render_template('quiz.html', questions=questions, unanswered=[], user_answers={}) 

@app.route("/practical", methods=["GET", "POST"])
def practical():
    tasks = load_practical_tasks()  # Загружаем задания
    
    if request.method == "POST":
        # Здесь будет обработка ответов
        pass
    
    return render_template("practical.html", tasks=tasks, enumerate=enumerate)  # Передаем tasks

if __name__ == "__main__":
    app.run(debug=True)


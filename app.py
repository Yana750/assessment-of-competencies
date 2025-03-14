from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = '062548ddaee0416eebce748db07012f1'  # Вставьте ваш секретный ключ

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
    # Выводим итоговый результат на главной странице
    total_score = session.get('total_score', None)
    return render_template('index.html', total_score=total_score)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()  # Загружаем вопросы из файла
    answers = load_answers()      # Загружаем правильные ответы
    if request.method == 'POST':
        score = 0
        total = len(questions)
        unanswered = []
        user_answers = {}  # Словарь для хранения ответов пользователя
        
        # Получаем ответы пользователя из формы
        for question in questions:
            user_answer = request.form.get(question['question'])  # Извлекаем ответ пользователя по вопросу
            correct_answer = answers.get(question['question'])  # Извлекаем правильный ответ из answers.json
            
            if user_answer:
                user_answers[question['question']] = user_answer  # Сохраняем ответ пользователя
                if user_answer == correct_answer:  # Сравниваем ответ с правильным
                    score += 1
            else:
                unanswered.append(question['question'])

        # Если есть вопросы без ответа
        if unanswered:
            return render_template('quiz.html', questions=questions, unanswered=unanswered, message="Вы не ответили на некоторые вопросы", user_answers=user_answers)
        
        # Применяем вашу формулу для оценки
        K_1 = (30 * score) / total  # Формула для оценки
        
        session['K_1'] = K_1  # Сохраняем результат теоретических знаний в сессии
        
        return render_template('result.html', score=score, total=total, K_1=K_1)
    
    return render_template('quiz.html', questions=questions, unanswered=[], user_answers={})

@app.route('/practical', methods=['GET', 'POST'])
def practical():
    tasks = load_practical_tasks()  # Загружаем практические задания
    user_answers = {}
    if request.method == "POST":
        answers = request.form.to_dict()  # Извлекаем все ответы пользователя
        difficulty = request.form.get('difficulty')  # Получаем сложность задания (если она есть)

        # Получаем задания в зависимости от сложности (например, "Обычный")
        task_list = tasks.get(difficulty, [])

        correct_count = 0
        total_tasks = len(task_list)

        # Проходим по каждому заданию
        for task in task_list:
            question = task["description"]
            correct_answer = task["answer"].strip()  # Правильный ответ
            user_answer = answers.get(question, "").strip()  # Ответ пользователя для текущего вопроса

            user_answers[question] = user_answer  # Сохраняем ответ пользователя

            if not user_answer:
                continue  # Если пользователь не ответил, пропускаем

            if user_answer == correct_answer:
                correct_count += 1  # Увеличиваем счетчик за правильный ответ
            elif user_answer in correct_answer:
                correct_count += 0.5  # Учитываем частичный ответ

        # Рассчитываем рейтинг выполнения практических заданий
        q1 = correct_count / total_tasks if total_tasks > 0 else 0  # Рейтинг выполнения
        k2 = 70 * q1  # Итоговая оценка для практических заданий

        session['K_2'] = k2  # Сохраняем оценку в сессии

        # Получаем результат теоретического теста из сессии
        K_1 = session.get('K_1', 0)  # Если теоретический результат еще не был сохранен, берем 0

        # Рассчитываем итоговую оценку S
        S = (0.3 * K_1) + (0.7 * k2)  # Формула для итогового балла

        return render_template('practical_result.html', k2=k2, q1=q1, S=S)

    return render_template('practical.html', tasks=tasks, enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)

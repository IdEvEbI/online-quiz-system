from app import app, mysql
from flask import render_template, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        question = request.form.get('question')

        # 插入题目到数据库
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO questions (content) VALUES (%s)", (question,))
        mysql.connection.commit()
        cursor.close()

        # 渲染成功页面
        return render_template('upload_success.html', message=f"题目已保存：{question}")
    return render_template('upload.html')

@app.route('/questions')
def list_questions():
    # 查询所有题目
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT content, created_at FROM questions")
    questions = cursor.fetchall()
    cursor.close()

    return render_template('questions.html', questions=questions)

@app.route('/practice')
def practice():
    # 随机抽取一条题目
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT content FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()

    # 检查是否有题目
    if question:
        return render_template('practice.html', question=question[0])
    return "暂无题目可练习"
from app import app
from flask import render_template, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        question = request.form.get('question')
        return f"收到题目：{question}"
    return render_template('upload.html')
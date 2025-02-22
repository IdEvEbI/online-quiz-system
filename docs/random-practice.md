# 实现学生随机练习功能

## 一、目标

1. 从数据库随机抽取题目供学生练习。
2. 在 **Flask** 中添加随机练习页面。
3. 更新首页增加练习入口。

## 二、开发日志

### 2.1 修改路由支持随机抽题

为了让学生能随机练习题目，我们需要在路由中添加一个新端点，从数据库中随机获取一条记录。

1. 更新 `app/routes.py`：

   ```python
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
   
           return f"题目已保存：{question}"
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
   ```

- **说明**：`ORDER BY RAND()` 实现随机抽取，`LIMIT 1` 限制返回一条。

### 2.2 创建随机练习模板

我们需要一个新模板来展示随机抽取的题目，保持简洁并提供返回链接。

1. 创建 `app/templates/practice.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>随机练习</title>
   </head>
   <body>
       <h1>随机练习</h1>
   
       <!-- 显示随机题目 -->
       <p>{{ question }}</p>
   
       <a href="/">返回首页</a>
   </body>
   </html>
   ```

   - **说明**：使用 **Jinja2** 的 `{{ question }}` 动态显示题目内容。

### 2.3 更新首页增加练习入口

为了方便访问练习页面，在首页导航中添加一个新链接。

1. 修改 `app/templates/index.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>在线题库系统</title>
   </head>
   <body>
       <h1>欢迎使用在线题库系统</h1>
   
       <!-- 导航链接 -->
       <a href="/upload">上传题目</a> | 
       <a href="/questions">查看题目</a> | 
       <a href="/practice">随机练习</a>
   </body>
   </html>
   ```

   - **说明**：新增 **随机练习** 链接，与现有功能并列。

### 2.4 启动和测试应用

启动应用并验证随机练习功能，确保数据库和服务器正常运行。

1. 执行终端命令：

   ```bash
   # 确保 Docker MySQL 运行
   docker start mysql-quiz
   
   # 激活虚拟环境
   source venv/bin/activate
   
   # 启动 Flask 应用
   python run.py
   ```

   - 输出类似：

     ```bash
     * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
     * Debugger is active!
     ```

## 三、验证结果与提交

### 3.1 验证结果

1. 访问 `http://127.0.0.1:5000/`：
   - 预期：显示 **欢迎使用在线题库系统** 及 **上传题目**、**查看题目**、**随机练习** 链接。
2. 点击 **随机练习**：
   - 预期：显示一条随机题目，或提示 **暂无题目可练习**（若数据库为空）。

### 3.2 提交到 GitHub

1. 执行提交：

   ```bash
   # 添加更改文件
   git add app/ docs/random-practice.md
   
   # 提交到 develop 分支
   git commit -m "实现学生随机练习功能，添加练习页面和入口"
   
   # 推送到远程
   git push origin develop
   ```

   - **说明**：同步代码和文档到远程仓库。

## 四、常见问题

- **无题目显示**：确保数据库有数据，运行 `INSERT INTO questions (content) VALUES ('测试题目');`。
- **500 错误**：检查 Docker 是否运行（`docker ps`）及主机是否为 `127.0.0.1`。
- **页面空白**：确认 `practice.html` 在 `app/templates` 下。

## 五、扩展阅读

- **SQL 随机查询**：[MySQL RAND()](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_rand)。
- **Flask 路由**：[Flask Routing](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.route)。
- **HTML 布局**：[MDN HTML 基础](https://developer.mozilla.org/zh-CN/docs/Learn/HTML)。

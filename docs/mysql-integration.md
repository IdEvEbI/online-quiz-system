# 连接 MySQL 数据库

## 一、目标

1. 在 **Flask** 中集成 **MySQL**。
2. 实现题目存储到数据库。
3. 支持从数据库读取题目。

## 二、开发日志

### 2.1 安装和配置依赖

为了连接 **MySQL**，我们需要安装必要的库并确保开发环境准备就绪。

1. 在终端执行以下命令：

   ```bash
   # 激活虚拟环境
   source venv/bin/activate
   
   # 安装 pkg-config，用于查找 MySQL 库
   brew install pkg-config
   
   # 安装 MySQL 开发库，确保 mysql_config 可用
   brew install mysql
   brew link mysql --force
   
   # 安装 Flask-MySQLdb，连接 Flask 和 MySQL
   pip install flask-mysqldb
   ```

   - **验证**：运行 `mysql_config --version`，预期类似 `9.2.0`。

### 2.2 配置 Flask 和 MySQL

我们需要在 **Flask** 中配置 **MySQL** 连接参数，确保能访问 **Docker** 中的数据库。

1. 修改 `app/__init__.py`：

   ```python
   from flask import Flask
   from flask_mysqldb import MySQL
   
   # 初始化 Flask 应用
   app = Flask(__name__)
   
   # 配置 MySQL 参数，使用 IP 避免 Socket 问题
   app.config['MYSQL_HOST'] = '127.0.0.1'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'root1234'
   app.config['MYSQL_DB'] = 'quiz_db'
   
   # 初始化 MySQL 连接
   mysql = MySQL(app)
   
   # 导入路由
   from app import routes
   ```

   - **说明**：`127.0.0.1` 强制使用 TCP，确保 **Docker** 容器可达。

### 2.3 创建数据库表和路由

这一步创建题目表并更新路由，使其支持数据库操作。

1. 创建表并配置路由：
   - 连接 MySQL：

     ```bash
     # 使用 IP 连接 Docker MySQL，密码为 root1234
     mysql -h 127.0.0.1 -u root -p
     ```

     - 在 MySQL 中执行：

       ```sql
       USE quiz_db;
       CREATE TABLE questions (
           id INT AUTO_INCREMENT PRIMARY KEY,
           content TEXT NOT NULL,
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );
       SHOW TABLES;
       ```

       - 预期：显示 `questions`。
   - 更新 `app/routes.py`：

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
     ```

### 2.4 创建和更新模板

我们需要创建题目列表模板并更新首页，添加查看功能。

1. 创建 `app/templates/questions.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>题目列表</title>
   </head>
   <body>
       <h1>题目列表</h1>

       <!-- 显示题目列表 -->
       <ul>
       {% for question in questions %}
           <li>{{ question[0] }} (创建时间: {{ question[1] }})</li>
       {% endfor %}
       </ul>

       <a href="/">返回首页</a>
   </body>
   </html>
   ```

2. 更新 `app/templates/index.html`：

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
       <a href="/questions">查看题目</a>
   </body>
   </html>
   ```

### 2.5 启动和测试应用

最后启动 Docker 和 Flask，测试数据库集成是否正常。

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
   - 预期：显示 **欢迎使用在线题库系统** 及 **上传题目**、**查看题目** 链接。
2. 点击 **上传题目**，输入并提交：
   - 预期：返回 **题目已保存：{输入的内容}**。
3. 点击 **查看题目**：
   - 预期：列出题目及创建时间。

### 3.2 提交到 GitHub

1. 执行提交：

   ```bash
   # 添加更改文件
   git add app/ docs/mysql-integration.md
   
   # 提交到 develop 分支
   git commit -m "集成 MySQL，支持题目存储和展示，修复 localhost 问题"
   
   # 推送到远程
   git push origin develop
   ```

## 四、常见问题

- **连接失败**：确认 `127.0.0.1` 和 Docker 容器运行（`docker ps`）。
- **表不存在**：重新执行 `CREATE TABLE`。
- **安装失败**：检查 `brew install mysql` 和 `pkg-config` 是否完成。

## 五、扩展阅读

- **MySQL 连接方式**：[Socket vs TCP](https://dev.mysql.com/doc/refman/8.0/en/connecting.html)。
- **Flask-MySQLdb**：[官方文档](https://flask-mysqldb.readthedocs.io/)。
- **Docker 网络**：[Docker Networking](https://docs.docker.com/network/)。

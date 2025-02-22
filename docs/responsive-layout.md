# 实现响应式布局

## 一、目标

1. 基于现有 **Bootstrap** 样式，添加 **H5** 支持。
2. 实现跨设备适配，优化移动端体验。
3. 保持 **PC** 端样式一致性。

## 二、开发日志

### 2.1 检查和优化 Bootstrap 配置

为了支持响应式布局，我们需要确保 **Bootstrap** 已正确配置，并测试现有样式在移动端的表现。

1. 验证 `app/__init__.py` 中的静态资源配置：

   ```python
   from flask import Flask
   from flask_mysqldb import MySQL
   from flask_assets import Environment, Bundle
   
   # 初始化 Flask 应用
   app = Flask(__name__)
   
   # 配置 MySQL
   app.config['MYSQL_HOST'] = '127.0.0.1'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'root1234'
   app.config['MYSQL_DB'] = 'quiz_db'
   
   # 初始化 MySQL
   mysql = MySQL(app)
   
   # 配置静态资源
   assets = Environment(app)
   css = Bundle('css/bootstrap.min.css', output='gen/styles.css')
   assets.register('css_all', css)
   
   # 导入路由
   from app import routes
   ```

   - **说明**：确保 CSS 文件加载正常，`Bootstrap` 默认支持响应式。

2. 检查 **Bootstrap** 文件是否存在：
   - 确认 `app/static/css/bootstrap.min.css` 已就位。
   - **说明**：无需额外操作，UI 优化步骤已完成。

### 2.2 更新页面模板支持响应式

我们调整所有页面模板，利用 **Bootstrap** 的网格系统和类，使其适配移动端，并优化上传成功提示。

1. 更新 `app/templates/index.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>在线题库系统</title>
   
     <!-- 引入 Bootstrap 样式 -->
     <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
   </head>
   
   <body>
     <div class="container mt-4">
       <h1>欢迎使用在线题库系统</h1>
       <nav class="mt-3 d-flex flex-column flex-md-row gap-2">
         <a href="/upload" class="btn btn-outline-primary">上传题目</a>
         <a href="/questions" class="btn btn-outline-primary">查看题目</a>
         <a href="/practice" class="btn btn-outline-primary">随机练习</a>
       </nav>
     </div>
   </body>
   
   </html>
   ```

   - **说明**：用 `d-flex` 和 `flex-column flex-md-row` 实现导航响应式。

2. 更新 `app/templates/upload.html` 和路由：
   - 修改 `app/routes.py` 中的 `upload`：

     ```python
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
     ```

   - 更新 `app/templates/upload.html`：

     ```html
     <!DOCTYPE html>
     <html lang="zh-CN">
     
     <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>上传题目</title>
     
       <!-- 引入 Bootstrap 样式 -->
       <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
     </head>
     
     <body>
       <div class="container mt-4">
         <h1>上传题目</h1>
         <form method="POST" class="mt-3">
           <div class="mb-3">
             <label class="form-label">题目内容：</label>
             <textarea name="question" class="form-control" rows="4"></textarea>
           </div>
           <div class="d-flex flex-column flex-md-row gap-2">
             <button type="submit" class="btn btn-primary">提交</button>
             <a href="/" class="btn btn-secondary">返回首页</a>
           </div>
         </form>
       </div>
     </body>
     
     </html>
     ```

   - 创建 `app/templates/upload_success.html`：

     ```html
     <!DOCTYPE html>
     <html lang="zh-CN">
     
     <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>上传成功</title>
     
       <!-- 引入 Bootstrap 样式 -->
       <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
     </head>
     
     <body>
       <div class="container mt-4">
         <h1 class="h3">上传成功</h1>
         <p class="text-break fs-5">{{ message }}</p>
         <div class="d-flex flex-column flex-md-row gap-2">
           <a href="/upload" class="btn btn-primary">继续上传</a>
           <a href="/" class="btn btn-secondary">返回首页</a>
         </div>
       </div>
     </body>
     
     </html>
     ```

   - **说明**：成功页面用 `fs-5` 和 `text-break` 确保文字响应式。

3. 更新 `app/templates/questions.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>题目列表</title>
   
     <!-- 引入 Bootstrap 样式 -->
     <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
   </head>
   
   <body>
     <div class="container mt-4">
       <h1>题目列表</h1>
       <ul class="list-group mt-3">
         {% for question in questions %}
         <li class="list-group-item">{{ question[0] }} <small class="text-muted">(创建时间: {{ question[1] }})</small></li>
         {% endfor %}
       </ul>
       <a href="/" class="btn btn-secondary mt-3">返回首页</a>
     </div>
   </body>
   
   </html>
   ```

   - **说明**：列表自适应，时间用 `text-muted` 显示。

4. 确认 `app/templates/practice.html` 与上一版本一致：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>随机练习</title>
   
     <!-- 引入 Bootstrap 样式 -->
     <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
   </head>
   
   <body>
     <div class="container mt-4">
       <h1>随机练习</h1>
       <div class="card mt-3">
         <div class="card-body">
           <p class="card-text">{{ question }}</p>
         </div>
       </div>
       <a href="/" class="btn btn-secondary mt-3">返回首页</a>
     </div>
   </body>
   
   </html>
   ```

   - **说明**：随机练习页面布局已经适配，无需修改。

### 2.3 启动和测试响应式效果

启动应用，验证页面在 **PC** 和移动端的显示效果，包括上传成功提示。

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

   - **说明**：用浏览器开发者工具（F12）切换**移动视图**测试。

## 三、验证结果与提交

### 3.1 验证结果

1. 在 **PC** 端访问 `http://127.0.0.1:5000/`：
   - 预期：导航按钮水平排列，布局清晰。
2. 在移动端（或模拟器）访问并上传题目：
   - 预期：成功提示文字大小适配，导航垂直排列。
3. 检查所有页面：
   - 预期：**上传题目**、**查看题目**、**随机练习** 均响应式显示。

### 3.2 提交到 GitHub

1. 执行提交：

   ```bash
   # 添加更改文件
   git add app/ docs/responsive-layout.md
   
   # 提交到 develop 分支
   git commit -m "实现响应式布局，优化 H5 适配，修复上传提示"
   
   # 推送到远程
   git push origin develop
   ```

   - **说明**：记录响应式优化和修复。

## 四、常见问题

- **文字未适配**：确认 `upload_success.html` 已创建并使用。
- **样式未加载**：检查 `bootstrap.min.css` 路径。
- **布局错乱**：确保 `d-flex` 和 `gap` 类正确应用。

## 五、扩展阅读

- **响应式设计**：[Bootstrap Grid](https://getbootstrap.com/docs/5.3/layout/grid/)。
- **移动优先**：[Mobile-First CSS](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Responsive/Mobile_first)。
- **浏览器调试**：[Chrome DevTools](https://developer.chrome.com/docs/devtools/)。

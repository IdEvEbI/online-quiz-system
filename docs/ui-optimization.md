# 优化用户界面

## 一、目标

1. 为题目上传和练习页面添加基础样式。
2. 优先优化 **PC** 端用户体验。
3. 使用 **Bootstrap** 提升界面美观性和交互性。

## 二、开发日志

### 2.1 引入 Bootstrap 样式框架

为了快速优化界面，我们引入 **Bootstrap**，一个流行的 CSS 框架，提供现成的样式和组件。

1. 在终端安装静态文件管理工具并下载 **Bootstrap**：

   ```bash
   # 激活虚拟环境
   source venv/bin/activate

   # 安装 Flask-Assets 用于管理静态资源
   pip install flask-assets

   # 下载 Bootstrap（可选，手动放入 static 文件夹也可）
   pip install bootstrap-flask
   ```

   - **说明**：`Flask-Assets` 帮助整合 CSS 和 JS，`Bootstrap-Flask` 提供集成支持。

2. 配置 `app/__init__.py` 以支持静态资源：

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

   - **说明**：添加 `assets` 管理 CSS 文件，确保样式加载。

3. 将 Bootstrap 文件放入 `app/static/css/`：
   - 从 [Bootstrap 官网](https://getbootstrap.com/docs/5.3/getting-started/download/) 下载 `bootstrap.min.css`。
   - 放入 `app/static/css/bootstrap.min.css`。

### 2.2 更新页面样式

依次优化**首页导航**、**上传题目**、**查看题目**和**随机练习** 4 个页面的显示效果。

1. 修改**首页导航** `app/templates/index.html` 页面的样式：

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
       <nav class="mt-3">
         <a href="/upload" class="btn btn-outline-primary me-2">上传题目</a>
         <a href="/questions" class="btn btn-outline-primary me-2">查看题目</a>
         <a href="/practice" class="btn btn-outline-primary">随机练习</a>
       </nav>
     </div>
   </body>
   
   </html>
   ```

   - **说明**：用 `btn-outline-primary` 替换纯链接，提升交互性。

2. 修改**上传题目** `app/templates/upload.html` 页面的样式：

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
         <button type="submit" class="btn btn-primary">提交</button>
       </form>
       <a href="/" class="btn btn-secondary mt-2">返回首页</a>
     </div>
   </body>
   
   </html>
   ```

   - **说明**：使用 `container` 和 `form-control` 类美化布局。

3. 修改**题目列表** `app/templates/questions.html` 页面的样式：

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
               <li class="list-group-item">{{ question[0] }} (创建时间: {{ question[1] }})</li>
           {% endfor %}
           </ul>
           <a href="/" class="btn btn-secondary mt-3">返回首页</a>
       </div>
   </body>
   </html>
   ```

   - **说明**：用 `list-group` 优化列表样式。

4. 修改**随机练习** `app/templates/practice.html` 页面的样式：

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

   - **说明**：用 `card` 组件包裹题目，增加视觉层次感。

### 2.3 启动和测试优化效果

启动应用，验证样式是否正确应用到所有页面。

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

   - **说明**：检查全部 4 个页面样式的加载情况。

## 三、验证结果与提交

### 3.1 验证结果

1. 访问 `http://127.0.0.1:5000/`：
   - 预期：首页显示优化后的导航按钮。
2. 点击 **上传题目**：
   - 预期：**表单和按钮样式**美观，布局清晰。
3. 点击 **查看题目**：
   - 预期：题目以**列表形式**展示，布局清晰。
4. 点击 **随机练习**：
   - 预期：题目以**卡片形式**展示，界面简洁。

### 3.2 提交到 GitHub

1. 执行提交：

   ```bash
   # 添加更改文件
   git add app/ docs/ui-optimization.md
   
   # 提交到 develop 分支
   git commit -m "优化用户界面，添加 Bootstrap 样式，优先 PC 端"
   
   # 推送到远程
   git push origin develop
   ```

   - **说明**：记录 UI 优化成果。

## 四、常见问题

- **样式未加载**：确认 `bootstrap.min.css` 在 `app/static/css/` 下。
- **页面错乱**：检查 HTML 是否正确引入 Bootstrap。
- **依赖错误**：确保 `pip install flask-assets` 和 `bootstrap-flask` 成功。

## 五、扩展阅读

- **Bootstrap 文档**：[Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)。
- **Flask-Assets**：[官方文档](https://flask-assets.readthedocs.io/)。
- **CSS 基础**：[MDN CSS 教程](https://developer.mozilla.org/zh-CN/docs/Learn/CSS)。

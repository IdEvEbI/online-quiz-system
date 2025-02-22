# 搭建 Flask 基础应用

## 一、目标

1. 用 **Flask** 创建一个基础 Web 应用。
2. 实现简单的首页和题目上传接口。
3. 在 **VSCode** 中配置开发环境。

## 二、开发日志

### 2.1 创建 Flask 应用结构

1. 在项目根目录下创建文件结构：

   ```bash
   mkdir -p app/templates app/static
   touch app/__init__.py app/routes.py run.py
   ```

   - 项目结构：

     ```bash
     online-quiz-system/
     ├── app/
     │   ├── __init__.py      # Flask 应用初始化
     │   ├── routes.py        # 路由定义
     │   ├── templates/       # HTML 模板目录
     │   └── static/          # 静态文件（如 CSS、JS）
     ├── run.py               # 启动文件
     ├── venv/                # 虚拟环境
     └── docs/
     ```

2. 编辑 `app/__init__.py` 初始化 Flask：

   ```python
   from flask import Flask

   app = Flask(__name__)

   from app import routes  # 导入路由
   ```

3. 编辑 `app/routes.py` 定义路由：

   ```python
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
   ```

4. 编辑 `run.py` 启动应用：

   ```python
   from app import app
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

### 2.2 创建 HTML 模板

1. 创建首页模板 `app/templates/index.html`：

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
       <a href="/upload">上传题目</a>
   </body>
   </html>
   ```

2. 创建上传页面 `app/templates/upload.html`：

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>上传题目</title>
   </head>
   <body>
       <h1>上传题目</h1>
       <form method="POST">
           <label>题目内容：</label><br>
           <textarea name="question" rows="4" cols="50"></textarea><br>
           <input type="submit" value="提交">
       </form>
       <a href="/">返回首页</a>
   </body>
   </html>
   ```

### 2.3 配置 VSCode

1. 安装推荐扩展：
   - **Python**（Microsoft）：代码补全和调试。
   - **GitLens**：查看 Git 历史。
2. 设置 **Python 解释器**：
   - 按 `Cmd + Shift + P`，输入 **Python: Select Interpreter**。
   - 选择 `./venv/bin/python3`。
3. （可选）启用调试：
   - 点击左侧 **运行和调试**，选择 **create a launch.json file**。
   - 会生成 `.vscode/launch.json`，内容如下：

     ```json
     {
         "version": "0.2.0",
         "configurations": [
             {
                 "name": "Run Flask App",
                 "type": "debugpy",
                 "request": "launch",
                 "program": "${workspaceFolder}/run.py",
                 "console": "integratedTerminal"
             }
         ]
     }
     ```

   - 打开 `run.py`，点击右上角 **三角形（运行）** 按钮即可运行。

### 2.4 运行与测试

1. 激活虚拟环境：

   ```bash
   source venv/bin/activate
   ```

2. 运行应用：

   ```bash
   python run.py
   ```

   - 输出类似：

     ```bash
     * Serving Flask app 'app'
     * Debug mode: on
     * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
     * Debugger is active!
     ```

## 三、验证结果与提交

### 3.1：验证结果

1. 打开浏览器，访问 `http://127.0.0.1:5000/`：
   - 预期：显示 **欢迎使用在线题库系统** 及 **上传题目** 链接。
2. 点击 **上传题目**，输入内容并提交：
   - 预期：页面返回 **收到题目：{输入的内容}**。
3. 检查 **VSCode**：
   - 代码高亮正常，解释器显示为虚拟环境。

### 3.2：提交到 GitHub

```bash
git add app/ run.py .vscode/launch.json docs/flask-base.md
git commit -m "搭建 Flask 基础应用，支持首页和上传接口"
git push origin develop
```

## 四、常见问题

- **404 Not Found**：检查路由拼写或文件路径是否正确。
- **模板未找到**：确保 `templates` 文件夹在 `app` 目录下，而非 `static`。
- **端口占用**：若 `5000` 端口被占，修改 `run.py` 为 `app.run(debug=True, port=5001)`。

## 五、扩展阅读

- **Flask 官方文档**：[Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/)。
- **VSCode Python 开发**：[官方指南](https://code.visualstudio.com/docs/python/python-tutorial)。
- **VSCode 调试**：[调试配置](https://code.visualstudio.com/docs/python/debugging)。
- **HTML 基础**：[MDN HTML 教程](https://developer.mozilla.org/zh-CN/docs/Learn/HTML)。

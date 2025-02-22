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
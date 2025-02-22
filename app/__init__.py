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
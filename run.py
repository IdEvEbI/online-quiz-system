from app import app
import logging

logging.basicConfig(level=logging.DEBUG)  # 捕获详细日志

if __name__ == '__main__':
    app.run(debug=True)
import logging.handlers
import os
import re

import dotenv
from flask import Flask

import route

dotenv.load_dotenv()

app = Flask(__name__)

DEBUG = os.environ.get('APP_ENV', 'production') == 'development'

# 加载路由
route.add_new_routes(app)

# 日志配置
if DEBUG == False:
    logger = logging.getLogger('werkzeug')
    handler = logging.handlers.TimedRotatingFileHandler(
        filename='log/app.log',
        when='midnight',
        backupCount=7,
        encoding='utf-8')
    handler.suffix = '%Y-%m-%d.log'
    # extMatch是编译好正则表达式，用于匹配日志文件名后缀
    # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    logger.addHandler(handler)

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=os.environ.get('PORT', 5000),
        debug=DEBUG
    )

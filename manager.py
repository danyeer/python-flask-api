
try:
    from werkzeug.contrib.fixers import ProxyFix
except ImportError:
    from werkzeug.middleware.proxy_fix import ProxyFix
from flask_script import Manager, Server

from app import create_app

# app = Flask(__name__)

"""
development:    开发环境
production:     生产环境
testing:        测试环境
default:        默认环境

"""
# 通过传入当前的开发环境，创建应用实例，不同的开发环境配置有不同的config。这个参数也可以从环境变量中获取
app = create_app('development')

app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)
manager.add_command("run", Server())

if __name__ == '__main__':
    manager.run()

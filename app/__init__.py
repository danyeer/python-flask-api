# -- coding: utf-8 --
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from app.component.auth import mount_route_meta_to_endpoint, load_endpint_infos
from app.component.error import APIException, RepeatException, ServerError
from app.component.logger import apply_request_log
from app.component.redprint import RedprintAssigner

# from app.config.setting import config

# 创建数据库
from app.extensions.api_docs.swagger import apply_swagger

db = SQLAlchemy()


def create_app(config_name):
    # 初始化
    app = Flask(__name__)
    load_config(app, config_name)

    # 注册所有蓝本
    regist_blueprints(app)
    register_plugin(app)

    return app


def load_config(app, config_name):
    # 导致指定的配置对象:创建app时，传入环境的名称
    if config_name == 'production':
        app.config.from_object('app.config.secure')
        app.config.from_object('app.config.setting')
    else:
        app.config.from_object('app.config.secure')
        app.config.from_object('app.config.setting')


def regist_blueprints(app):
    # 导入蓝本对象
    # 方式一
    # from app.api import api

    # 方式二：这样，就不用在app/api/__init__.py（创建蓝本时）里面的最下方单独引入各个视图模块了
    # from app.api.views import api
    # from app.api.errors import api

    # 注册api蓝本,url_prefix为所有路由默认加上的前缀
    # app.register_blueprint(api, url_prefix='/api')

    # 注册蓝图
    app.config.from_object('app.extensions.api_docs.config')
    assigner = RedprintAssigner(app=app, rp_api_list=app.config['ALL_RP_API_LIST'])

    # 将红图的每个api的tag注入SWAGGER_TAGS中
    @assigner.handle_rp
    def handle_swagger_tag(api):
        app.config['SWAGGER_TAGS'].append(api.tag)

    bp_list = assigner.create_bp_list()
    for url_prefix, bp in bp_list:
        app.register_blueprint(bp, url_prefix=url_prefix)
    mount_route_meta_to_endpoint(app)
    load_endpint_infos(app)


def register_plugin(app):
    apply_json_encoder(app)  # JSON序列化
    apply_cors(app)  # 应用跨域扩展，使项目支持请求跨域
    connect_db(app)  # 连接数据库
    handle_error(app)  # 统一处理异常

    # Debug模式(以下为非必选应用，且用户不可见)
    # apply_default_view(app)  # 应用默认路由
    # apply_orm_admin(app)  # 应用flask-admin, 可以进行简易的 ORM 管理
    apply_swagger(app)  # 应用flassger, 可以查阅Swagger风格的 API文档
    if app.config['DEBUG']:
        apply_request_log(app)  # 打印请求日志


def apply_json_encoder(app):
    from app.component.json_encoder import JSONEncoder
    app.json_encoder = JSONEncoder


def apply_cors(app):
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})


def connect_db(app):
    db.init_app(app)
    #  初始化使用
    with app.app_context():  # 手动将app推入栈
        db.create_all()  # 首次模型映射(ORM ==> SQL),若无则建表


def handle_error(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            return APIException(code=e.code, error_code=1007, msg=e.description)
        elif isinstance(e, IntegrityError) and 'Duplicate entry' in e.orig.errmsg:
            return RepeatException(msg='数据的unique字段重复')
        else:
            if not app.config['DEBUG']:
                print(e)
                return ServerError()  # 未知错误(统一为服务端异常)
            else:
                raise e

# def create_tables(app):
#     """
#     根据模型，创建表格（可以有两种写法）
#     1、模型必须在create_all方法之前导入，模型类声明后会注册到db.Model.metadata.tables属性中
#     不导入模型模块，就不会执行模型中的代码，也就无法完成注册。
#     2、但是，如果db是在模型模块中创建的，同时在此处 from app.models import db 引用db,则就实现了
#     模型和数据库的绑定，不需要再单独导入模型模块了。
#     """
#     db.create_all(app=app)

# -- coding: utf-8 --
# 废弃
from flask import jsonify
# from . import api


# 使用errorhandler装饰器，只有蓝本才能触发处理程序
# 要想触发全局的错误处理程序，要用app_errorhandler

# @api.app_errorhandler(404)
# def page_not_found(e):
#     """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
#     return jsonify({'error': '没有找到您想要的资源', 'code': '404', 'data': ''})
#
#
# @api.app_errorhandler(500)
# def internal_server_error(e):
#     """这个handler可以catch住所有的abort(500)和raise exeception."""
#     return jsonify({'error': '服务器内部错误', 'code': '500', 'data': ''})

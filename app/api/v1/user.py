# -- coding: utf-8 --
"""
@Time: 2020/8/20 16:20
@Author: w
"""
from flask import g

from app.component.error import Success
from app.component.token_auth import auth
from app.extensions.api_docs.redprint import Redprint
from app.extensions.api_docs.v1 import user as api_doc
from app.models.user import User

api = Redprint(name='user', module='用户', api_doc=api_doc)


@api.route('', methods=['GET'])
@api.doc(auth=True)
@auth.login_required
def get_user():
    '''查询自身'''
    user = User.get(id=g.user.id)
    return Success(user)

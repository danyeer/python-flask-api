# _*_ coding: utf-8 _*_
"""

"""
from app.component.db import db
from app.libs.enums import ScopeEnum, ClientTypeEnum
from app.models.user import User
from app.models.identity import Identity



class UserDao():

    # 获取用户列表
    @staticmethod
    def get_user_list(page, size):
        paginator = User.query \
            .filter_by(auth=ScopeEnum.COMMON.value) \
            .paginate(page=page, per_page=size, error_out=True)
        paginator.hide('address')
        return {
            'total': paginator.total,
            'current_page': paginator.page,
            'items': paginator.items
        }

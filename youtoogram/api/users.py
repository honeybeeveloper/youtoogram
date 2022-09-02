import datetime

from flask import (
    jsonify,
    request,
)

from youtoogram.api.route import Route
from youtoogram.common.exception import (
    DuplicatedUserId,
    PasswordLengthViolation,
    UserNotFound,
    UserIdLengthViolation
)
from youtoogram.feature.users import Users


class UsersAPI(object):
    @staticmethod
    def sign_up():
        now = datetime.datetime.now()
        data = request.json
        # step 1. 유효성(길이) 체크
        UsersAPI.check_form_length(data=data)
        # step 2. 사용자 아이디 중복 체크
        if UsersAPI.is_exists_user_id(data=data):
            raise DuplicatedUserId('user-id is duplicated!')

        Users.create(data=data, now=now)
        return jsonify('successfully sign up!')

    @staticmethod
    def check_form_length(data):
        # 1. user-id
        length = len(data['user_id'])
        if length < 4 or length > 20:
            raise UserIdLengthViolation('check the user-id length!')
        # 2. password
        length = len(data['password'])
        if length < 4 or length > 20:
            raise PasswordLengthViolation('check the password length!')

    @staticmethod
    def is_exists_user_id(data):
        return Users.is_exists_user_id(data['user_id'])

    @staticmethod
    def delete_id():
        now = datetime.datetime.now()
        data = request.json
        # step 1. 사용자 확인
        if not UsersAPI.is_exists_user_id(data=data):
            return UserNotFound(f'user not found!')

        Users.delete(data['user_id'])
        return jsonify('successfully delete id!')


routes = [
    Route(uri='/users', view_func=UsersAPI.sign_up, methods=['POST']),
    Route(uri='/users', view_func=UsersAPI.delete_id, methods=['DELETE'])
]

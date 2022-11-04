import datetime

import bcrypt
from flask import (
    jsonify,
    request,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from youtoogram.api.route import Route
from youtoogram.common.exception import (
    DuplicatedUserId,
    PasswordLengthViolation,
    UserNotFound,
    UserIdLengthViolation,
    UnauthorizedException
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
        if UsersAPI.is_exists_user_id(user_id=data['user_id']):
            raise DuplicatedUserId('user-id is duplicated!')
        # step 3. 비밀번호 암호화
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode()

        Users.create(data=data, now=now)
        return {'user_id': data['user_id']}

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
    def is_exists_user_id(user_id):
        return Users.is_exists_user_id(user_id)

    @staticmethod
    @jwt_required()
    def delete_id():
        sign_in_id = get_jwt_identity()
        # step 1. 사용자 확인
        if not UsersAPI.is_exists_user_id(user_id=sign_in_id):
            return UserNotFound(f'user not found!')

        Users.delete(sign_in_id)
        return {'user_id': sign_in_id}

    @staticmethod
    def sign_in():
        data = request.json
        user_id = data['user_id']
        password = data['password']
        returned_user_id, returned_password = Users.signin(user_id)

        if bcrypt.checkpw(password.encode('utf-8'), returned_password.encode('utf-8')):
            access_token = create_access_token(identity=returned_user_id, expires_delta=datetime.timedelta(seconds=60*60))
            return jsonify({
                'access_token': access_token
            })
        else:
            raise UnauthorizedException('Please check your password!')


routes = [
    Route(uri='/users', view_func=UsersAPI.sign_up, methods=['POST']),
    Route(uri='/users', view_func=UsersAPI.delete_id, methods=['DELETE']),
    Route(uri='/signin', view_func=UsersAPI.sign_in, methods=['POST'])
]

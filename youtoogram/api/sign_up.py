import datetime

from flask import (
    jsonify,
    request,
)

from youtoogram.api.route import Route
from youtoogram.common.exception import (
    DuplicatedUserId,
    PasswordLengthViolation,
    UserIdLengthViolation
)
from youtoogram.feature.sign_up import SignUp


class SignUpAPI(object):
    @staticmethod
    def sign_up():
        now = datetime.datetime.now()
        data = request.json
        # step 1. 유효성(길이) 체크
        SignUpAPI.check_form_length(data=data)
        # step 2. 사용자 아이디 중복 체크
        SignUpAPI.check_user_id_duplication(data=data)

        SignUp.create(data=data, now=now)
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
    def check_user_id_duplication(data):
        if SignUp.is_exists_user_id(data['user_id']):
            raise DuplicatedUserId('user-id is duplicated!')


routes = [
    Route(uri='/users/sign-up', view_func=SignUpAPI.sign_up, methods=['POST'])
]

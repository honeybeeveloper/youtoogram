import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from youtoogram.api.route import Route
from youtoogram.common.exception import BadRequest, UserNotFound
from youtoogram.feature.follow import Follow
from youtoogram.feature.users import Users


class FollowAPI(object):
    @staticmethod
    @jwt_required()
    def follow():
        now = datetime.datetime.now()
        data = request.json
        # check user-id == follow-id
        if data['user_id'] == data['follow_id']:
            raise BadRequest('Can not follow yourself.')
        # check the follow-id existence
        if not Users.is_exists_user_id(data['follow_id']):
            raise UserNotFound('follow-id is not found!')

        login_id = get_jwt_identity()
        data['user_id'] = login_id
        Follow.create(data=data, now=now)
        return jsonify(f'{data["user_id"]} follow {data["follow_id"]} successfully!')

    @staticmethod
    @jwt_required()
    def unfollow():
        data = request.json
        # check user-id == follow-id
        if data['user_id'] == data['follow_id']:
            raise BadRequest('can not unfollow yourself.')

        # check the follow-id existence
        if not Follow.is_exists_follow_id(data['user_id'], data['follow_id']):
            raise UserNotFound('follow-id is not found!')

        login_id = get_jwt_identity()
        Follow.delete(login_id, data['follow_id'])
        return jsonify(f'{data["user_id"]} unfollow {data["follow_id"]} successfully!')


routes = [
    Route(uri='/follow', view_func=FollowAPI.follow, methods=['POST']),
    Route(uri='/follow', view_func=FollowAPI.unfollow, methods=['DELETE'])
]

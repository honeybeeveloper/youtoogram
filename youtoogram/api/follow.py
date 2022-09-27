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
        login_id = get_jwt_identity()
        data = request.json

        # check login_id == follow-id
        if login_id == data['follow_id']:
            raise BadRequest('Can not follow yourself.')
        # check the follow-id existence
        if not Users.is_exists_user_id(data['follow_id']):
            raise UserNotFound('follow-id is not found!')

        data['user_id'] = login_id
        Follow.create(data=data, now=now)
        return {'user_id': login_id, 'follow_id': data['follow_id']}

    @staticmethod
    @jwt_required()
    def unfollow():
        data = request.json
        login_id = get_jwt_identity()
        # check login_id == unfollow-id
        if login_id == data['unfollow_id']:
            raise BadRequest('Can not unfollow yourself.')

        # check the follow-id existence
        if not Follow.is_exists_follow_id(login_id, data['unfollow_id']):
            raise UserNotFound(f'{data["unfollow_id"]} is not found!')

        Follow.delete(login_id, data['unfollow_id'])
        return {'user_id': login_id, 'unfollow_id': data['unfollow_id']}


routes = [
    Route(uri='/follow', view_func=FollowAPI.follow, methods=['POST']),
    Route(uri='/follow', view_func=FollowAPI.unfollow, methods=['DELETE'])
]

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
        sign_in_id = get_jwt_identity()
        data = request.json

        # check sign_in_id == follow-id
        if sign_in_id == data['follow_id']:
            raise BadRequest('Can not follow yourself.')
        # check the follow-id existence
        if not Users.is_exists_user_id(data['follow_id']):
            raise UserNotFound('follow-id is not found!')

        data['user_id'] = sign_in_id
        Follow.create(data=data, now=now)
        return {'user_id': sign_in_id, 'follow_id': data['follow_id']}

    @staticmethod
    @jwt_required()
    def unfollow():
        data = request.json
        sign_in_id = get_jwt_identity()
        # check sign_in_id == unfollow-id
        if sign_in_id == data['unfollow_id']:
            raise BadRequest('Can not unfollow yourself.')

        # check the follow-id existence
        if not Follow.is_exists_follow_id(sign_in_id, data['unfollow_id']):
            raise UserNotFound(f'{data["unfollow_id"]} is not found!')

        Follow.delete(sign_in_id, data['unfollow_id'])
        return {'user_id': sign_in_id, 'unfollow_id': data['unfollow_id']}


routes = [
    Route(uri='/follow', view_func=FollowAPI.follow, methods=['POST']),
    Route(uri='/follow', view_func=FollowAPI.unfollow, methods=['DELETE'])
]

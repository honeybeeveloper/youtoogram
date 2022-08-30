import datetime

from flask import jsonify, request

from youtoogram.api.route import Route
from youtoogram.common.exception import BadRequest, UserNotFound
from youtoogram.feature.follow import Follow
from youtoogram.feature.sign_up import SignUp


class FollowAPI(object):
    @staticmethod
    def follow():
        now = datetime.datetime.now()
        data = request.json
        # check user-id == follow-id
        if data['user_id'] == data['follow_id']:
            raise BadRequest('can not follow yourself.')
        # check the follow-id duplication
        if not SignUp.is_exists_user_id(data['follow_id']):
            raise UserNotFound('follow-id is not found!')

        Follow.create(data=data, now=now)
        return jsonify(f'{data["user_id"]} follow {data["follow_id"]} successfully!')


routes = [
    Route(uri='/follow/addition', view_func=FollowAPI.follow, methods=['POST'])
]

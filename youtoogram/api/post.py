import datetime

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from youtoogram.api.route import Route
from youtoogram.common.exception import LengthViolation
from youtoogram.database.utility import to_dict
from youtoogram.feature.post import Post


class PostAPI(object):
    @staticmethod
    @jwt_required()
    def add_post():
        now = datetime.datetime.now()
        data = request.json
        # check gram length
        PostAPI.check_gram_length(data['gram'])
        # login id is user_id
        login_id = get_jwt_identity()
        data['user_id'] = login_id
        # TODO : photo_1 경로 -> form-data
        post_id = Post.create(data, now)
        return {'user_id': login_id, 'post_id': post_id}

    @staticmethod
    def check_gram_length(gram):
        length = len(gram)
        print(f'gram length is {length}')
        if length > 300:
            raise LengthViolation('gram length must be less than 300!')

    @staticmethod
    @jwt_required()
    def delete_post():
        data = request.json
        # login id is user_id
        login_id = get_jwt_identity()
        Post.delete(data['post_id'], login_id)
        return {'user_id': login_id, 'post_id': data['post_id']}

    @staticmethod
    @jwt_required()
    def update_post():
        data = request.json
        # login id is user_id
        login_id = get_jwt_identity()
        data['user_id'] = login_id
        Post.update(data)
        return {'user_id': login_id, 'post_id': data['post_id'], 'gram': data['gram']}

    @staticmethod
    @jwt_required()
    def timeline():
        # login id is user_id
        login_id = get_jwt_identity()
        user_id = login_id

        date_to = datetime.datetime.now()
        date_from = date_to - datetime.timedelta(days=10)
        # TODO : check this query!
        rows = Post.timeline(user_id, date_from, date_to)
        results = [to_dict(obj) for obj in rows]
        print(results)
        return jsonify(results)


routes = [
    Route(uri='/post', view_func=PostAPI.add_post, methods=['POST']),
    Route(uri='/post', view_func=PostAPI.delete_post, methods=['DELETE']),
    Route(uri='/post', view_func=PostAPI.update_post, methods=['PATCH']),
    Route(uri='/timeline', view_func=PostAPI.timeline, methods=['GET'])
]
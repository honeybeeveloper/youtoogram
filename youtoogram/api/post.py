import datetime

from flask import request, jsonify

from youtoogram.api.route import Route
from youtoogram.common.exception import LengthViolation
from youtoogram.feature.post import Post


class PostAPI(object):
    @staticmethod
    def add_post():
        now = datetime.datetime.now()
        data = request.json
        # check gram length
        PostAPI.check_gram_length(data['gram'])
        Post.create(data, now)
        return jsonify(f'Gram is posted successfully!')

    @staticmethod
    def check_gram_length(gram):
        length = len(gram)
        print(f'gram length is {length}')
        if length > 300:
            raise LengthViolation('gram length must be less than 300!')

    @staticmethod
    def delete_post():
        data = request.json
        Post.delete(data['id'], data['user_id'])
        return jsonify(f'Gram is deleted successfully!')

    @staticmethod
    def update_post():
        data = request.json
        Post.update(data)
        return jsonify(f'Gram is updated successfully!')


routes = [
    Route(uri='/post', view_func=PostAPI.add_post, methods=['POST']),
    Route(uri='/post', view_func=PostAPI.delete_post, methods=['DELETE']),
    Route(uri='/post', view_func=PostAPI.update_post, methods=['PATCH'])
]
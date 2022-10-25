import datetime
import os

from collections import defaultdict
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from youtoogram import config
from youtoogram.api.route import Route
from youtoogram.common.util import create_dir, save_to_jpg
from youtoogram.common.exception import FileNotFound, LengthViolation
from youtoogram.database.utility import to_dict
from youtoogram.feature.post import Post


class PostAPI(object):
    @staticmethod
    @jwt_required()
    def add_post():
        now = datetime.datetime.now()
        form = request.form
        # check gram length
        PostAPI.check_gram_length(form.get('gram'))
        data = defaultdict(str)
        data['gram'] = form.get('gram')
        # login id is user_id
        data['user_id'] = get_jwt_identity()
        # post_id
        data['post_id'] = Post.assign_id()
        PostAPI.handle_photos(data)

        post_id = Post.create(data, now)
        assert data['post_id'] == post_id
        return {'user_id': data['user_id'], 'post_id': data['post_id']}

    @staticmethod
    def check_gram_length(gram):
        length = len(gram) if gram else 0
        if length > 300:
            raise LengthViolation('gram length must be less than 300!')

    @staticmethod
    def handle_photos(data):
        # 파일 여러개 있을 수 있다 (최대 5개)
        cnt = 1
        files = request.files
        if files:
            today = datetime.date.today().strftime('%Y%m%d')
            original_dir = os.path.join(config.output_basedir, today, data['user_id'])
            create_dir(original_dir)

        for key, file in files.items():
            filename = file.filename
            if not filename.endswith(tuple(config.support_image_format)):
                raise FileNotFound('Check the image file format.')

            # file naming rule : {post_id}_{number}.jpg
            name = str(data['post_id']) + '_' + str(cnt)
            # 원본 이미지 저장
            path = save_to_jpg(file, original_dir, name)
            data[f'photo_{cnt}'] = path
            cnt += 1

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

# TODO : change
# delete : /post/<post_id>
# modify : /post/<post_id>
routes = [
    Route(uri='/post', view_func=PostAPI.add_post, methods=['POST']),
    Route(uri='/post', view_func=PostAPI.delete_post, methods=['DELETE']),
    Route(uri='/post', view_func=PostAPI.update_post, methods=['PATCH']),
    Route(uri='/timeline', view_func=PostAPI.timeline, methods=['GET'])
]
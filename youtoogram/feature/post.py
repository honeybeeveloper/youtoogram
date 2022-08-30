import datetime

from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Post(object):
    @staticmethod
    def create(data, now=datetime.datetime.now()):
        print(f'Post create now : {now}')
        db_session.add(entity.Post(user_id=data['user_id'], gram=data['gram'],
                                   photo_1=data['photo_1'], photo_2=data['photo_2'],
                                   photo_3=data['photo_3'], photo_4=data['photo_4'],
                                   photo_5=data['photo_5'], created_at=now))
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def delete(id, user_id):
        db_session.query(entity.Post)\
            .filter(entity.Post.id == id)\
            .filter(entity.Post.user_id == user_id)\
            .delete()
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def update(data, now=datetime.datetime.now()):
        db_session.query(entity.Post)\
            .filter(entity.Post.id == int(data['id']))\
            .filter(entity.Post.user_id == data['user_id'])\
            .update({entity.Post.gram: data['gram'],
                     entity.Post.photo_1: data['photo_1'],
                     entity.Post.photo_2: data['photo_2'],
                     entity.Post.photo_3: data['photo_3'],
                     entity.Post.photo_4: data['photo_4'],
                     entity.Post.photo_5: data['photo_5'],
                     entity.Post.modified_at: now})
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')
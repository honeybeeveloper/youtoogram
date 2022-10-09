import datetime

from sqlalchemy import func, subquery
from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Post(object):
    @staticmethod
    def create(data, now=datetime.datetime.now()):
        print(f'Post create now : {now}')
        p = entity.Post(user_id=data['user_id'], gram=data['gram'],
                        created_at=now, modified_at=now)
        db_session.add(p)
        try:
            db_session.commit()
            db_session.refresh(p)
            return p.id
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
            .filter(entity.Post.id == int(data['post_id']))\
            .filter(entity.Post.user_id == data['user_id'])\
            .update({entity.Post.gram: data['gram'],
                     entity.Post.modified_at: now})
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def timeline(user_id, date_from, date_to):
        return db_session.query(entity.Post.id, entity.Post.user_id, entity.Post.gram, entity.Post.modified_at)\
                .outerjoin(entity.Follow, entity.Follow.follow_id == entity.Post.user_id, isouter=True)\
                .filter((entity.Follow.user_id == user_id) | (entity.Post.user_id == user_id))\
                .filter(entity.Post.modified_at.between(date_from, date_to))\
                .order_by(entity.Post.id.desc())\
                .all()

    @staticmethod
    def get_recent_post_id(user_id):
        sub_stmt = db_session.query(func.max(entity.Post.id).label('max_post_id')).filter(entity.Post.user_id == user_id).subquery()
        recent_id, recent_gram, = db_session.query(sub_stmt.c.max_post_id, entity.Post.gram).filter(entity.Post.id == sub_stmt.c.max_post_id).one()
        return recent_id, recent_gram


if __name__ == '__main__':
    recent, gram = Post.get_recent_post_id('honeybeeveloper')
    print(recent, gram)
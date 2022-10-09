import datetime

from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.test_unit.test_database import entity
from youtoogram.test_unit.test_database.connection import db_session


class Follow(object):
    @staticmethod
    def test_create(data, now=datetime.datetime.now()):
        print(f'Follow create now : {now}')
        db_session.add(entity.Follow(user_id=data['user_id'],
                                     follow_id=data['follow_id'],
                                     created_at=now))
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def test_is_exists_follow_id(user_id, follow_id):
        q = db_session.query(entity.Follow)\
            .filter(entity.Follow.user_id == user_id)\
            .filter(entity.Follow.follow_id == follow_id)
        is_exists = db_session.query(q.exists()).scalar()
        return is_exists

    @staticmethod
    def test_delete(user_id, follow_id):
        db_session.query(entity.Follow)\
            .filter(entity.Follow.user_id == user_id)\
            .filter(entity.Follow.follow_id == follow_id)\
            .delete()

        db_session.commit()

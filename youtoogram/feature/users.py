import datetime

from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Users(object):
    @staticmethod
    def create(data, now=datetime.datetime.now()):
        print(f'SignUp create now : {now}')
        db_session.add(entity.Users(user_id=data['user_id'],
                                    password=data['password'],
                                    name=data['name'],
                                    nickname=data['nickname'],
                                    email=data['email'],
                                    phone=data['phone'],
                                    profile=data['profile'],
                                    created_at=now
                                    ))
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def is_exists_user_id(user_id):
        q = db_session.query(entity.Users).filter(entity.Users.user_id == user_id)
        is_exists = db_session.query(q.exists()).scalar()
        return is_exists

    @staticmethod
    def delete(user_id):
        db_session.query(entity.Users).filter(entity.Users.user_id == user_id).delete()
        db_session.commit()

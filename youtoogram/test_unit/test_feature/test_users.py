import datetime

from sqlalchemy.exc import IntegrityError, NoResultFound

from youtoogram.common.exception import IntegrityException, UserNotFound
from youtoogram.test_unit.test_database import entity
from youtoogram.test_unit.test_database.connection import db_session


class Users(object):
    @staticmethod
    def test_create(data, now=datetime.datetime.now()):
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
    def test_is_exists_user_id(user_id):
        q = db_session.query(entity.Users).filter(entity.Users.user_id == user_id)
        is_exists = db_session.query(q.exists()).scalar()
        return is_exists

    @staticmethod
    def test_delete(user_id):
        db_session.query(entity.Users).filter(entity.Users.user_id == user_id).delete()
        db_session.commit()

    @staticmethod
    def test_signin(user_id, now=datetime.datetime.now()):
        print(f'Sign in create now : {now}')
        try:
            user_id, password, = db_session.query(entity.Users.user_id, entity.Users.password)\
                                    .filter(entity.Users.user_id == user_id).one()
            return user_id, password
        except NoResultFound:
            raise UserNotFound('User Not Found!')

    @staticmethod
    def test_get_user(user_id):
        try:
            user_id, name, phone = db_session.query(entity.Users.user_id, entity.Users.name, entity.Users.phone)\
                                    .filter(entity.Users.user_id == user_id)\
                                    .one()
            return user_id, name, phone
        except NoResultFound:
            raise UserNotFound('User Not Found')
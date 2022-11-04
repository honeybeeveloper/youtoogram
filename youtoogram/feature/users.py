from datetime import datetime

from sqlalchemy.exc import IntegrityError, NoResultFound

from youtoogram.common.exception import IntegrityException, UserNotFound
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Users(object):
    @staticmethod
    def create(data, now=None):
        """사용자를 생성한다

        Args:
            data (_type_): 회원가입 요청한 사용자의 정보를 가진 딕셔너리
            now (_type_, optional): 회원가입 시도한 시간
                                    디폴트 값은 None

        Raises:
            IntegrityException:
        """
        if now is None:
            now = datetime.now()
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
        """아이디가 DB에 있는지 확인

        Args:
            user_id (_type_): 아이디

        Returns:
            _type_: 아이디 존재 여부
        """        
        q = db_session.query(entity.Users).filter(entity.Users.user_id == user_id)
        is_exists = db_session.query(q.exists()).scalar()
        return is_exists

    @staticmethod
    def delete(user_id):
        """사용자를 삭제한다

        Args:
            user_id (_type_): 삭제할 아이디
        """        
        db_session.query(entity.Users).filter(entity.Users.user_id == user_id).delete()
        db_session.commit()

    @staticmethod
    def signin(user_id, now=None):
        """로그인 위해 아이디와 비밀번호를 조회한다.

        Args:
            user_id (_type_): 로그인할 아이디
            now (_type_, optional): 로그인 시도한 시간
                                    디폴트 값은 None

        Raises:
            UserNotFound: 로그인할 아이디가 DB에 없으면 발생하는 예외

        Returns:
            _type_: 아이디, 비밀번호
        """        
        if now is None:
            now = datetime.now()
        print(f'Sign in create now : {now}')
        try:
            user_id, password, = db_session.query(entity.Users.user_id, entity.Users.password)\
                                    .filter(entity.Users.user_id == user_id).one()
            return user_id, password
        except NoResultFound:
            raise UserNotFound('User Not Found!')
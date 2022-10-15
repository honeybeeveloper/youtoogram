from datetime import datetime

from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Follow(object):
    @staticmethod
    def create(data, now=None):
        """팔로우 등록한다

        Args:
            data (_type_): 팔로우 관련 데이터 담긴 딕셔너리
            now (_type_, optional): 팔로우 등록 시도한 시간
                                    디폴트값은 None

        Raises:
            IntegrityException:
        """

        if now is None:
            now = datetime.now()
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
    def is_exists_follow_id(user_id, follow_id):
        """이미 팔로우했는지 여부 조회

        Args:
            user_id (_type_): 로그인한 아이디
            follow_id (_type_): 팔로우할 아이디

        Returns:
            _type_: 기존 팔로우 여부 반환
        """
        q = db_session.query(entity.Follow)\
            .filter(entity.Follow.user_id == user_id)\
            .filter(entity.Follow.follow_id == follow_id)
        is_exists = db_session.query(q.exists()).scalar()
        return is_exists

    @staticmethod
    def delete(user_id, unfollow_id):
        """팔로우 삭제한다

        Args:
            user_id (_type_): 로그인한 아이디
            follow_id (_type_): 언팔로우할 아이디
        """
        db_session.query(entity.Follow)\
            .filter(entity.Follow.user_id == user_id)\
            .filter(entity.Follow.follow_id == unfollow_id)\
            .delete()

        db_session.commit()

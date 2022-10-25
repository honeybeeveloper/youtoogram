from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.schema import Sequence

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Post(object):
    @staticmethod
    def assign_id():
        assign_id, = db_session.query(Sequence('post_id_seq').next_value()).one()
        return assign_id

    @staticmethod
    def create(data, now=None):
        """게시글을 등록한다

        Args:
            data (_type_): 등록할 게시글 정보 담긴 딕셔너리
            now (_type_, optional): 게시글 등록 시도한 시간
                                    디폴트 값은 None

        Raises:
            IntegrityException: _description_

        Returns:
            _type_: 등록한 게시글의 id
        """
        if now is None:
            now = datetime.now()
        print(f'Post create now : {now}')
        p = entity.Post(id=data['post_id'],
                        user_id=data['user_id'],
                        gram=data['gram'] if data['gram'] else None,
                        photo_1=data['photo_1'] if data['photo_1'] else None,
                        photo_2=data['photo_2'] if data['photo_2'] else None,
                        photo_3=data['photo_3'] if data['photo_3'] else None,
                        photo_4=data['photo_4'] if data['photo_4'] else None,
                        photo_5=data['photo_5'] if data['photo_5'] else None,
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
        """게시글을 삭제한다

        Args:
            id (_type_): 삭제할 게시글의 아이디
            user_id (_type_): 로그인한 아이디

        Raises:
            IntegrityException:
        """
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
    def update(data, now=None):
        """게시글을 수정한다

        Args:
            data (_type_): 수정할 게시글의 정보 담긴 딕셔너리
            now (_type_, optional): 게시글 수정 시도한 시간
                                    디폴트값은 None

        Raises:
            IntegrityException:
        """
        if now is None:
            now = datetime.now()
        print(f'Post update now : {now}')
        db_session.query(entity.Post)\
            .filter(entity.Post.id == int(data['post_id']))\
            .filter(entity.Post.user_id == data['user_id'])\
            .update({entity.Post.gram: data['gram'] if data['gram'] else None,
                     entity.Post.photo_1: data['photo_1'] if data['photo_1'] else None,
                     entity.Post.photo_2: data['photo_2'] if data['photo_2'] else None,
                     entity.Post.photo_3: data['photo_3'] if data['photo_3'] else None,
                     entity.Post.photo_4: data['photo_4'] if data['photo_4'] else None,
                     entity.Post.photo_5: data['photo_5'] if data['photo_5'] else None,
                     entity.Post.modified_at: now})
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

    @staticmethod
    def timeline(user_id, date_from, date_to):
        """타임라인을 조회한다

        Args:
            user_id (_type_): 로그인한 아이디
            date_from (_type_): 조회할 게시글의 수정시간(시작)
            date_to (_type_): 조회할 게시글의 수정시간(종료)

        Returns:
            _type_: 타임라인에 보여질 게시글들
        """
        return db_session.query(entity.Post.id, entity.Post.user_id, entity.Post.gram,
                                entity.Post.photo_1, entity.Post.photo_2, entity.Post.photo_3,
                                entity.Post.photo_4, entity.Post.photo_5, entity.Post.modified_at)\
                .outerjoin(entity.Follow, entity.Follow.follow_id == entity.Post.user_id, isouter=True)\
                .filter((entity.Follow.user_id == user_id) | (entity.Post.user_id == user_id))\
                .filter(entity.Post.modified_at.between(date_from, date_to))\
                .order_by(entity.Post.id.desc())\
                .all()

    @staticmethod
    def get_recent_post_id(user_id):
        """로그인한 아이디가 등록한 최근 게시글의 아이디

        Args:
            user_id (_type_): 로그인한 아이디

        Returns:
            _type_: 최근 게시글 아이디, 최근 게시글
        """
        sub_stmt = db_session.query(func.max(entity.Post.id).label('max_post_id')).filter(entity.Post.user_id == user_id).subquery()
        recent_id, recent_gram, = db_session.query(sub_stmt.c.max_post_id, entity.Post.gram).filter(entity.Post.id == sub_stmt.c.max_post_id).one()
        return recent_id, recent_gram


if __name__ == '__main__':
    recent, gram = Post.get_recent_post_id('honeybeeveloper')
    print(recent, gram)
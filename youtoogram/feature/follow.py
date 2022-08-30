import datetime

from sqlalchemy.exc import IntegrityError

from youtoogram.common.exception import IntegrityException
from youtoogram.database import entity
from youtoogram.database.connection import db_session


class Follow(object):
    @staticmethod
    def create(data, now=datetime.datetime.now()):
        print(f'Follow create now : {now}')
        db_session.add(entity.Follow(user_id=data['user_id'],
                                     follow_id=data['follow_id'],
                                     created_at=now))

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise IntegrityException('check the data!')

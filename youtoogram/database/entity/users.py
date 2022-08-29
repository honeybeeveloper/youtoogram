from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    Column,
    PrimaryKeyConstraint,
    Sequence,
    UniqueConstraint,
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
    String,
)

from youtoogram.database.entity.base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='users_pk')
    user_id = Column(String)
    UniqueConstraint('user_id', name='users_user_id_key')
    password = Column(String)
    name = Column(String)
    nickname = Column(String)
    email = Column(String)
    phone = Column(String)
    profile = Column(String)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    post = relationship('Post', back_populates='users', cascade='all, delete-orphan')
    follow = relationship('Follow', back_populates='users', cascade='all, delete-orphan')

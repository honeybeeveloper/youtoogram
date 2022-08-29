from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    Sequence,
)
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    DateTime
)

from youtoogram.database.entity.base import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='post_pk')
    user_id = Column(String,
                     ForeignKey('users.user_id',
                                name='post_user_id_fk',
                                onupdate='CASCADE',
                                ondelete='CASCADE'))
    gram = Column(String)
    photo_1 = Column(String)
    photo_2 = Column(String)
    photo_3 = Column(String)
    photo_4 = Column(String)
    photo_5 = Column(String)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

    users = relationship('Users', back_populates='post', cascade='save-update')

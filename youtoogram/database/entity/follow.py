from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    Sequence,
    UniqueConstraint,
)
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    DateTime,
)

from youtoogram.database.entity.base import Base


class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, Sequence('follow_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='follow_pk')
    user_id = Column(String,
                     ForeignKey('users.user_id',
                                name='follow_user_id_fk',
                                onupdate='CASCADE',
                                ondelete='CASCADE'))
    follow_id = Column(String)
    UniqueConstraint('user_id', 'follow_id', name='follow_user_id_follow_id_key')
    created_at = Column(DateTime, default=func.now())

    users = relationship('Users', back_populates='follow', cascade='save-update')

from sqlalchemy.engine.row import Row

from youtoogram.database.entity.base import Base


def to_dict(tuple):
    """
    Convert a SQLAlchemy object to a dictionary
    :return: dictionary
    """
    if isinstance(tuple, Base):
        return tuple.to_dict()
    elif isinstance(tuple, Row):
        dic = {}
        for key, value in tuple._mapping.items():
            if isinstance(value, Base) or isinstance(value, Row):
                dic[key] = to_dict(value)
            else:
                dic[key] = value
        return dic
    raise RuntimeError(f'Dictionary converter not available for type {type(tuple)}')

from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def to_dict(self):
        """
            convert an entity object to dictionary
        """
        dic = {}
        for col_attr in inspect(self).mapper.column_attrs:
            col_val = getattr(self, col_attr.key)
            print(f'col_val : {col_val}')


# 상속클래스들을 자동으로 인지하고 알아서 매핑해준다.
Base = declarative_base(cls=Base)
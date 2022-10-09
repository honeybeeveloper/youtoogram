from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker


config = {"database": {}}
config["database"]["user"] = 'postgres'
config["database"]["password"] = 'sweetjoohyun41!'
config["database"]["host"] = '127.0.0.1'
config["database"]["port"] = 5432
config["database"]["database"] = 'youtoogram_test'


def create_db_engine():
    return create_engine(url=f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@'
                             f'{config["database"]["host"]}:{config["database"]["port"]}/{config["database"]["database"]}',
                         echo=False,
                         pool_size=5,
                         max_overflow=10,
                         pool_recycle=3600)


engine = create_db_engine()

db_session = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker


# TODO : config 파일로 따로 뺄 것
config = {"database": {}}
config["database"]["user"] = 'postgres'
config["database"]["password"] = 'sweetjoohyun41!'
config["database"]["host"] = '127.0.0.1'
config["database"]["port"] = 5432
config["database"]["database"] = 'youtoogram'


def create_db_engine():
    # https://docs.sqlalchemy.org/en/14/core/pooling.html
    return create_engine(url=f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@'
                             f'{config["database"]["host"]}:{config["database"]["port"]}/{config["database"]["database"]}',
                         echo=False,
                         # the size of the pool to be maintained, defaults to 5
                         pool_size=5,
                         # When the number of checked-out connections reaches the size set in pool_size,
                         # additional connections will be returned up to this limit.
                         # Defaults to 10
                         max_overflow=10,
                         # connection that has been open for more than one hour will be invalidated and replaced
                         pool_recycle=3600)


engine = create_db_engine()

# 동일한 thread 에서의 session 충돌 방지를 위해 scoped_session 을 많이 사용한다.
# 하나의 thread 에서 동일한 session 을 이용해서 각기 다른 작업을 해야 할 경우
# session 을 파라미터로 넘겨줘서 session 을 유지하는 경우가 많은데
# scoped_session 과 session_maker 를 활용해서 간단하게 코드를 작성할 수가 있다.
db_session = scoped_session(sessionmaker(bind=engine))

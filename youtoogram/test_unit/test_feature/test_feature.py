import bcrypt
import datetime
import pytest

from flask_jwt_extended import create_access_token, get_jwt_identity

from youtoogram.test_unit.test_database.connection import db_session
from youtoogram.test_unit.test_feature.test_follow import Follow
from youtoogram.test_unit.test_feature.test_post import Post
from youtoogram.test_unit.test_feature.test_users import Users


@pytest.fixture
def follow():
    return Follow


@pytest.fixture
def post():
    return Post


@pytest.fixture
def users():
    return Users


def setup_function():
    # 테스트 데이터 추가
    test_user = {
        "user_id": "test_user",
        "password": "1234",
        "name": "테스터",
        "nickname": "테스터",
        "email": "tester@gmail.com",
        "phone": "01012345678",
        "profile": ""
    }
    test_user['password'] = bcrypt.hashpw(test_user['password'].encode('utf-8'),
                                          bcrypt.gensalt()).decode()
    Users.test_create(test_user, datetime.datetime.now())


# [Persistence] 회원가입 테스트
def test_insert_user(users):
    test_user = {
        "user_id": "test_user2",
        "password": "1234",
        "name": "테스터2",
        "nickname": "테스터2",
        "email": "tester@gmail.com",
        "phone": "01012345678",
        "profile": ""
    }
    test_user['password'] = bcrypt.hashpw(test_user['password'].encode('utf-8'), bcrypt.gensalt()).decode()
    users.test_create(test_user)
    user_id, name, phone = users.test_get_user(test_user['user_id'])
    assert test_user['user_id'] == user_id and test_user['name'] == name and test_user['phone'] == phone


# [Persistence] 로그인 테스트
def test_login(users):
    test_user = {
        "user_id": "test_user",
        "password": "1234"
    }
    user_id, password = users.test_login(test_user['user_id'])
    assert test_user['user_id'] == user_id and bcrypt.checkpw(test_user['password'].encode('utf-8'), password.encode('utf-8'))
    

# [Persistence] 팔로우 테스트
def test_follow(follow):
    data = {
        "user_id": "test_user",
        "follow_id": "test_user2"
    }
    follow.test_create(data)
    assert follow.test_is_exists_follow_id(data['user_id'], data['follow_id'])


# [Persistence] 언팔로우 테스트
def test_unfollow(follow):
    data = {
        "user_id": "test_user",
        "follow_id": "test_user2"
    }
    follow.test_delete(data['user_id'], data['follow_id'])
    assert not follow.test_is_exists_follow_id(data['user_id'], data['follow_id'])


# [Persistence] 게시글등록 테스트
def test_register_post(post):
    data = {
        "user_id": "test_user",
        "gram": "I will be rich!!"
    }
    post_id = post.test_create(data)
    return_post_id, _ = post.test_get_recent_post(data['user_id'])
    assert post_id == return_post_id


# [Persistence] 게시글수정 테스트
def test_modify_post(post):
    return_post_id, _ = post.test_get_recent_post('test_user')
    data = {
        "user_id": "test_user",
        "post_id": return_post_id,
        "gram": "I will be attractive person!!"
    }
    post.test_update(data)
    _, return_post_gram = post.test_get_recent_post(test_user)
    assert data['gram'] == return_post_gram





def teardown_function():
    db_session.execute('TRUNCATE users CASCADE')
    db_session.execute('TRUNCATE follow CASCADE')
    db_session.execute('TRUNCATE post CASCADE')
    db_session.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')
    db_session.execute('ALTER SEQUENCE post_id_seq RESTART WITH 1')
    db_session.execute('ALTER SEQUENCE follow_id_seq RESTART WITH 1')
    db_session.commit()
    db_session.close()

import pytest
from flask import Flask, json
from flask_jwt_extended import JWTManager

import sys
sys.path.append(r'D:\Python\toy-project\youtoogram')
from youtoogram.api import users, follow, post


access_token = None
post_id = None


@pytest.fixture
def test_api():
    app = Flask(__name__)
    app.config['TEST'] = True
    app.config['JSON_AS_ASCII'] = False
    # app.json.ensure_ascii = False

    routes = users.routes + follow.routes + post.routes
    [app.add_url_rule(rule=r.uri, view_func=r.view_func, methods=r.methods) for r in routes]

    app.config['JWT_SECRET_KEY'] = 'honeybee1!2@3#youtoogram'
    app.config['JWT_ALGORITHM'] = 'HS256'
    JWTManager(app)

    t_api = app.test_client()
    return t_api


def test_signin(test_api):
    test_user = {
        "user_id": "test_user",
        "password": "1234",
        "name": "테스터",
        "nickname": "테스터",
        "email": "tester@gmail.com",
        "phone": "01012345678",
        "profile": ""
    }
    resp = test_api.post('/users',
                         content_type='application/json',
                         data=json.dumps(test_user))
    assert resp.status_code == 200


def test_login(test_api):
    global access_token
    test_user = {
        "user_id": "test_user",
        "password": "1234"
    }
    resp = test_api.post('/login',
                         content_type='application/json',
                         data=json.dumps(test_user))
    assert resp.status_code == 200
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']


def test_follow(test_api):
    global access_token
    follow = {"follow_id": "honeybeeveloper"}
    resp = test_api.post('/follow',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {access_token}'},
                         data=json.dumps(follow))
    assert resp.status_code == 200


def test_add_post(test_api):
    global access_token, post_id
    post = {"gram": "This is a test gram!!"}
    resp = test_api.post('/post',
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {access_token}'},
                         data=json.dumps(post))
    assert resp.status_code == 200
    resp_json = json.loads(resp.data.decode('utf-8'))
    post_id = resp_json['post_id']


def test_update_post(test_api):
    global access_token, post_id
    update_post = {"post_id": post_id,
                   "gram": 'This is a updated gram!!'}
    resp = test_api.patch('/post',
                          content_type='application/json',
                          headers={'Authorization': f'Bearer {access_token}'},
                          data=json.dumps(update_post))
    assert resp.status_code == 200


def test_delete_post(test_api):
    global access_token, post_id
    delete_post = {"post_id": post_id}
    resp = test_api.delete('/post',
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {access_token}'},
                           data=json.dumps(delete_post))
    assert resp.status_code == 200


def test_timeline(test_api):
    global access_token
    resp = test_api.get('/timeline',
                        headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200


def test_unfollow(test_api):
    global access_token
    unfollow = {"unfollow_id": "honeybeeveloper"}
    resp = test_api.delete('/follow',
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {access_token}'},
                           data=json.dumps(unfollow))
    assert resp.status_code == 200


def test_signout(test_api):
    global access_token
    resp = test_api.delete('/users',
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200


if __name__ == '__main__':
    test_api.run(host='0.0.0.0', port=5000, debug=True)
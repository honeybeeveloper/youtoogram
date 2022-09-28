from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from youtoogram.api import users, follow, post
from youtoogram.common.exception import CustomException


app = Flask(__name__)
# This is deprecated and will be removed in Flask 2.3
app.config['JSON_AS_ASCII'] = False
# app.json.ensure_ascii = False

routes = users.routes + follow.routes + post.routes
[app.add_url_rule(rule=r.uri, view_func=r.view_func, methods=r.methods) for r in routes]

# set secret-key for JWT
# TODO : secure config 로 빼기
app.config['JWT_SECRET_KEY'] = 'honeybee1!2@3#youtoogram'
app.config['JWT_ALGORITHM'] = 'HS256'
JWTManager(app)


@app.route('/test')
def test():
    return jsonify('successful test!')


@app.errorhandler(CustomException)
def handle_error(e):
    return jsonify(e.to_dict()), e.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
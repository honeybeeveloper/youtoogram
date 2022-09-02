from flask import Flask, jsonify

from youtoogram.api import users, follow, post
from youtoogram.common.exception import CustomException


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

routes = users.routes + follow.routes + post.routes
[app.add_url_rule(rule=r.uri, view_func=r.view_func, methods=r.methods) for r in routes]


@app.route('/test')
def test():
    return jsonify('successful test!')


@app.errorhandler(CustomException)
def handle_error(e):
    return jsonify(e.to_dict()), e.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
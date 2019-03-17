from flask import Flask, jsonify, request
from conf import SECRET_KEY

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': SECRET_KEY,
})


@app.route('/')
def index():
    secret_key = request.form.get('SECRET_KEY')
    if secret_key is None:
        return jsonify({
            'code': 400,
            'msg': 'The parameter SECRET_KEY is required',
        }), 400
    if SECRET_KEY != secret_key:
        return jsonify({
            'code': 401,
            'msg': '',
        }), 401
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

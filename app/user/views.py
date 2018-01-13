from flask import render_template
from app.user import user


@user.route('/')
def index():
	print('__name__', __name__)
	return render_template('index.html')


@user.before_request
def defore_request():
	print('defore_request_blueprint')

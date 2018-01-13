#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj
#date 2017-11-21


from flask 		import Flask
from app.index	import index
from app.user 	import user


app = Flask (
	__name__,
	template_folder = 'templates',
	static_folder = 'static'
)
# @app.before_request
def before_request():
	print('before_request')

# @app.teardown_request
def teardown_request(exception):
	print('teardown_request')

app.register_blueprint(index)
app.register_blueprint(user, url_prefix='/user')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

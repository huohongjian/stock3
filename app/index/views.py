from flask		import render_template
from app.index	import index


@index.route('/')
def index():
	return render_template('user/index.html')



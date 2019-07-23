from bottle import route, request, debug, run, template, static_file


@route('/images/<filename>')
def send_image(filename):
	return static_file(filename, root='./images/')

@route('/')
def index():
	return template('weatherMap.tpl')

debug(True)
run(reloader=True)
'''
WATCH MY ANIME
'''
from json import dumps
from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from secrets import mail
from watch import Watch
from anime import Anime
from models import db

app = Flask(__name__)

'''
Email Settings
'''
app.config['MAIL_SERVER'] = 'smtp.mandrillapp.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail['username']
app.config['MAIL_PASSWORD'] = mail['password']

mailman = Mail(app)

'''
REST API
'''
@app.route('/api/fetch/<path:email>', methods = ['GET'])
def api_fetch(email):
	if email:
		watching = Anime.fetchUpdates(email)
		watchList = []

		for watch in watching:
			watch.last_update = watch.watched
			watch.save()

			watchList.append(watch.toJSON())

		return dumps(watchList)

	return redirect('/')

'''
Unsubscribe from the Service
'''
@app.route('/unsubscribe/<path:h>', methods = ['GET'])
def unsubscribe(h):
	if h:
		watch = Anime.getUnique(h)

		if watch.count() == 1:
			watch = watch.first()
			watch.delete()

			flash('You are no longer watching [{0}] {1}.'.format(watch.subber, watch.anime))

	return redirect('/')

'''
Render FAQ
'''
@app.route('/faq', methods = ['GET'])
def faq():
	return render_template('faq.html', title = 'Frequently Asked Questions')

'''
Render Contact
'''
@app.route('/contact', methods = ['GET'])
def contact():
	return render_template('contact.html', title = 'Contact')

'''
Render Index Page
'''
@app.route('/', methods = ['GET', 'POST'])
@app.route('/<path:status>', methods = ['GET'])
def index(status = None):
	add = Watch(request.form)

	if request.method == 'GET' and status:
		return redirect('/')

	if request.method == 'POST' and add.validate():
		anime = Anime(add.name.data, add.subber.data, add.format.data, add.quality.data, add.email.data)
		anime.save()

		flash(
			'''
			You are now watching [{0}] {1}. To unwatch this click <a href="/unsubscribe/{2}">here</a>.
			'''.format(add.subber.data, add.name.data, anime.h)
		)

		return redirect('/success')

	return render_template('index.html', title = 'Watch My Anime', form = add, status = status)

if __name__ == '__main__':
	app.debug = True
	app.run(host ='0.0.0.0')
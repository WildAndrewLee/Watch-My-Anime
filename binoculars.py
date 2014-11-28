from flask import Flask
from flask_mail import Message
from anime import Anime
from models import db
from app import mailman, app
import sys
import feedparser
import re
import time

'''
Cron Job to Check Anime
'''
delimit = '[ _]'
sys.stdout = open('../cron.log', 'a')

print 'Beginning Cron at ' + time.strftime('%I:%M:%S') + ' on ' + time.strftime('%m/%d/%Y')

feed = feedparser.parse('http://www.nyaa.se/?page=rss')

for anime in feed['entries']:	
	name = anime['title']

	# Regular expression verified using http://www.regexr.com/
	# on every episode of anime I have downloaded.
	regex = r'\[(.+)\][ _]+(.+?)[ _]*-?[ _]*(\d+)[ _]*((\[|\().*((480|720|1080|BD)p?).*(\]|\)))?([ _]*\[.+][ _]*)?\.(\w+)'

	details = re.search(regex, name)

	try:
		if details and len(details.groups()) == 10:
			subber = details.group(1)
			title = details.group(2)
			episode = str(int(details.group(3)))
			quality = details.group(7)
			format = details.group(10).upper()

			match = Anime.getAllMatches(subber, title, episode, quality, format)

			for watch in match:
				message = Message(
					'New Episode of {0} Available'.format(watch.anime),
					sender = 'A Letter Bee <no-reply@watchmyani.me>',
				)

				message.add_recipient(watch.email)

				message.html = '''
				Episode {0} of {1} is now available. Click <a href="{2}">here</a> to download it now.
				<br />
				<br />
				<small>To stop receiving notifications click <a href="http://watchmyani.me/unsubscribe/{3}">here</a>.</small>
				'''.format(episode, title, anime['links'][0]['href'], watch.h)

				with app.app_context():
					mailman.send(message)

				watch.watched = episode
				watch.save()

	except (KeyboardInterrupt, SystemExit):
		raise

	except Exception as e:
		print e
		raise

print 'Finished Cron at ' + time.strftime('%I:%M:%S') + ' on ' + time.strftime('%m/%d/%Y')

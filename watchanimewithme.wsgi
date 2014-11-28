'''
WSGI For Watch My Anime
'''
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/watchanimewithme/")

from app import app as application
application.secret_key = 'what key?'
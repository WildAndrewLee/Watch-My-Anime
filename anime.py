from models import db
from sqlalchemy import or_
import uuid

'''
Anime Database Model
'''
class Anime(db.Model):
	__tablename__ = 'watching'
	id = db.Column(db.Integer, primary_key = True)
	anime = db.Column(db.String(255))
	subber = db.Column(db.String(255))
	format = db.Column(db.String(255))
	quality = db.Column(db.String(255))
	email = db.Column(db.String(255))
	watched = db.Column(db.Integer)
	h = db.Column(db.String(255))

	@staticmethod
	def getAllMatches(subber, title, episode, quality, format):
		filtered = Anime.query.filter(
			Anime.subber == subber,
			Anime.anime == title,
			Anime.watched < episode,
			Anime.format == format
		)

		if quality:
			filtered = filtered.filter(
				or_(Anime.quality == 'N/A', Anime.quality == quality)
			)

		return filtered

	@staticmethod
	def getUnique(h):
		return Anime.query.filter(
			Anime.h == h
		)
	 
	def __init__(self, anime, subber, format, quality, email):
		self.anime = anime
		self.subber = subber
		self.format = format
		self.quality = quality
		self.email = email
		self.watched = -1
		self.h = uuid.uuid4()

	def save(self):
		db.session.merge(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()
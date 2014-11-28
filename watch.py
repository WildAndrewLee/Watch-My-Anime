from wtforms import Form, TextField, SelectField, validators

'''
Form for adding an anime to your watch list
'''
class Watch(Form):
	_method = 'POST'
	_action = '/'

	name = TextField('Name', validators = [
		validators.Required(message = 'You must enter the name of an anime.')
	])

	subber = TextField('Sub Group', validators = [
		validators.Required(message = 'You must enther the name of a sub group.')
	])

	format = TextField('Format', default = 'MKV', validators = [
		validators.Optional()
	])

	quality = SelectField('Quality', choices = [
		('1080', '1080p'),
		('720', '720p'),
		('480', '480p'),
		('N/A', 'N/A')
	], validators = [
		validators.Optional()
	])

	email = TextField('Email', validators = [
		validators.Email(message = 'You must enter a valid email.'),
		validators.Required(message = 'You must enter a valid email.')
	])
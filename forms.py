# forms.py

from wtforms import Form, StringField, SelectField, PasswordField, BooleanField, DateTimeField, validators
from wtforms.fields.html5 import EmailField
from flask_security import LoginForm
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from models import Environment, Version, SwpNumber, OsbIntegration, OdsIntegration, OssIntegration

class ExtendedLoginForm(LoginForm):
    email = EmailField('Email', [validators.DataRequired(message='email is required '), validators.Email(message='invalid email address')])
    password = PasswordField('Password', [validators.DataRequired(message='password is required')])
    remember = BooleanField('Remember Me')

class RequestSearchForm(Form):
	choices = [('Environment Number', 'Environment Number'),
				('Version', 'Version')]
	select = SelectField('Search for request:', choices=choices)
	search = StringField('')

def envreq_choices():
	return Environment.query

def version_choices():
	return Version.query

def swpnumber_choices():
	return SwpNumber.query

def osb_choices():
	return OsbIntegration.query

def ods_choices():
	return OdsIntegration.query

def oss_choices():
	return OssIntegration.query

class EnvironmentRequestForm(Form):
	environment = QuerySelectField(query_factory=envreq_choices, allow_blank=False, get_pk=lambda x: x.id)
	requestedby = StringField('Requested By')
	version = StringField('Version', id="versionbox")
	swp_number = QuerySelectMultipleField(query_factory=swpnumber_choices, allow_blank=False, get_pk=lambda x: x.id, id="selectswp")
	start_date = StringField('Start Date')
	delivery_date = StringField('Delivery Date')
	backup_db = BooleanField('Backup Database?')
	keep_data = BooleanField('Keep Environment Data?')
	keep_ld = BooleanField('Keep Logical Date?')
	osb_integration = QuerySelectField(query_factory=osb_choices, allow_blank=False, get_pk=lambda x: x.id)
	ods_integration = QuerySelectField(query_factory=ods_choices, allow_blank=False, get_pk=lambda x: x.id)
	oss_integration = QuerySelectField(query_factory=oss_choices, allow_blank=False, get_pk=lambda x: x.id)
	source_uat_ref = QuerySelectField(query_factory=envreq_choices, allow_blank=False, get_pk=lambda x: x.id)
	delivery_notification = StringField('Deliver Notification')
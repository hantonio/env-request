# forms.py

from wtforms import Form, StringField, SelectField, PasswordField, BooleanField, DateTimeField, validators
from wtforms.fields.html5 import EmailField
from flask_security import LoginForm
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from models import Environment, Version, SwpNumber, OsbIntegration, OdsIntegration, OssIntegration
from wtforms.validators import InputRequired

class ExtendedLoginForm(LoginForm):
    email = EmailField('Email', [validators.DataRequired(message='email is required '), validators.Email(message='invalid email address')], render_kw={"class": "form-control"})
    password = PasswordField('Password', [validators.DataRequired(message='password is required')], render_kw={"class": "form-control"})
    remember = BooleanField('Remember Me', render_kw={"class": "checkbox"})

class RequestSearchForm(Form):
	choices = [('Environment Number', 'Environment Number'),
				('Version', 'Version')]
	select = SelectField('Search for request:', choices=choices, render_kw={"class": "form-control"})
	search = StringField('', render_kw={"class": "form-control"})

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
	environment = QuerySelectField(query_factory=envreq_choices, allow_blank=False, get_pk=lambda x: x.id, render_kw={"class": "form-control"}, validators=[InputRequired()])
	requestedby = StringField('Requested By', render_kw={"class": "form-control"}, validators=[InputRequired()])
	version = StringField('Version', id="versionbox", render_kw={"class": "form-control"}, validators=[InputRequired()])
	swp_number = QuerySelectMultipleField(query_factory=swpnumber_choices, allow_blank=False, get_pk=lambda x: x.id, id="selectswp", render_kw={"class": "form-control"}, validators=[InputRequired()])
	start_date = StringField('Start Date', render_kw={"class": "form-control"}, validators=[InputRequired()])
	delivery_date = StringField('Delivery Date', render_kw={"class": "form-control"}, validators=[InputRequired()])
	backup_db = BooleanField('Backup Database?', render_kw={"class": "checkbox"})
	keep_data = BooleanField('Keep Environment Data?', render_kw={"class": "checkbox"})
	keep_ld = BooleanField('Keep Logical Date?', render_kw={"class": "checkbox"})
	osb_integration = QuerySelectField(query_factory=osb_choices, allow_blank=False, get_pk=lambda x: x.id, render_kw={"class": "form-control"}, validators=[InputRequired()])
	ods_integration = QuerySelectField(query_factory=ods_choices, allow_blank=False, get_pk=lambda x: x.id, render_kw={"class": "form-control"}, validators=[InputRequired()])
	oss_integration = QuerySelectField(query_factory=oss_choices, allow_blank=False, get_pk=lambda x: x.id, render_kw={"class": "form-control"}, validators=[InputRequired()])
	source_uat_ref = QuerySelectField(query_factory=envreq_choices, allow_blank=False, get_pk=lambda x: x.id, render_kw={"class": "form-control"}, validators=[InputRequired()])
	delivery_notification = StringField('Deliver Notification', render_kw={"class": "form-control"})
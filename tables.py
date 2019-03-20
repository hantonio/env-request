# tables.py

from flask_table import Table, Col, LinkCol

class Results(Table):
	id = Col('ID', show=False)
	env = Col('Environment')
	requestedby = Col('Requested By')
	version = Col('Version')
	swp_number = Col('SWP Number')
	start_date = Col('Start Date')
	delivery_date = Col('Delivery Date')
	backup_db = Col('Backup Database?')
	keep_data = Col('Keep Environment Data?')
	keep_ld = Col('Keep Logical Date?')
	osb_integration = Col('OSB Integration')
	ods_integration = Col('ODS Integration')
	oss_integration = Col('OSS Integration')
	source_uat_ref = Col('Source UAT REF')
	delivery_notification = Col('Delivery Notification to')
	edit = LinkCol('Edit', 'edit_req', url_kwargs=dict(id='id'))
	delete = LinkCol('Delete', 'delete_req', url_kwargs=dict(id='id'))
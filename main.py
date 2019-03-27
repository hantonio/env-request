# test.py

from app import app
from app import db
from db_setup import init_db, db_session
from forms import EnvironmentRequestForm, RequestSearchForm
from flask import flash, render_template, request, redirect
from models import User, Role, EnvironmentRequest, Environment
from tables import Results
from sqlalchemy.orm.session import make_transient, make_transient_to_detached
#from flask_sqlalchemy import SQLAlchemy
#from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, utils, login_required
from sqlalchemy.orm.base import NEVER_SET
from sqlalchemy import inspect
import json

init_db()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=encrypted_password)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    search = RequestSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/request_results')
def search_results(search):
    results=[]
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Version':
            qry = db_session.query(EnvironmentRequest).filter(EnvironmentRequest.version.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Environment Number':
            qry = db_session.query(EnvironmentRequest).join(Environment).filter(Environment.number == int(search_string))
            results = qry.all()
    else:
        qry = db_session.query(EnvironmentRequest)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/request/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_req(id):
    req = db_session.query(EnvironmentRequest).filter(EnvironmentRequest.id==id).first()

    if req:
        form = EnvironmentRequestForm(formdata=request.form, obj=req)
        
        if request.method == 'GET':
            form.keep_data.data = req.keep_data
            form.keep_ld.data = req.keep_ld
            form.backup_db.data = req.backup_db

        if request.method == 'POST' and form.validate():
            _ = req.environment_id
            _ = req.ods_id
            _ = req.osb_id
            _ = req.oss_id
            _ = req.swp_number

            db_session.expire(req, ['environment'])
            db_session.expire(req, ['swp_number'])    
            db_session.expire(req, ['ods_integration'])    
            db_session.expire(req, ['osb_integration'])
            db_session.expire(req, ['oss_integration'])

            make_transient(req)
            make_transient_to_detached(req)

            inspect(req).committed_state.update(id=NEVER_SET)
            inspect(req).committed_state.update(environment=NEVER_SET)
            inspect(req).committed_state.update(swp_number=NEVER_SET)
            inspect(req).committed_state.update(osb_integration=NEVER_SET)
            inspect(req).committed_state.update(ods_integration=NEVER_SET)
            inspect(req).committed_state.update(oss_integration=NEVER_SET)
            req.environment = form.environment.data
            req.requestedby = form.requestedby.data
            req.swp_number = form.swp_number.data
            req.zones = form.zones.data
            req.version = str(form.swp_number.data).split()[0]
            req.start_date = form.start_date.data
            req.delivery_date = str(form.delivery_date.data)
            req.backup_db = form.backup_db.data
            req.keep_data = form.keep_data.data
            req.keep_ld = form.keep_ld.data
            req.osb_integration = form.osb_integration.data
            req.ods_integration = form.ods_integration.data
            req.oss_integration = form.oss_integration.data                        

            req.source_uat_ref = str(form.source_uat_ref.data)
            req.delivery_notification = form.delivery_notification.data 
            req.approval = False
            
            current_session=db_session.object_session(req)
            current_session.commit()
            flash('Environment Request updated successfully!')
            return redirect('/')
        return render_template('edit_request.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/request/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_req(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(EnvironmentRequest).filter(EnvironmentRequest.id==id)
    req = qry.first()

    if req:
        form = EnvironmentRequestForm(formdata=request.form, obj=req)
        if request.method == 'GET':
            form.keep_data.data = req.keep_data
            form.keep_ld.data = req.keep_ld
            form.backup_db.data = req.backup_db
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(req)
            db_session.commit()

            flash('Request deleted successfully!')
            return redirect('/')
        return render_template('delete_request.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


@app.route('/request/new', methods=['GET', 'POST'])
@login_required
def new_request():
    form = EnvironmentRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        req = EnvironmentRequest()
        save_request(req, form, new=True)
        flash('Environment Request created successfully!')
        return redirect('/')    
    return render_template('new_request.html', form=form)


def save_request(req, form, new=False):
    req.environment = form.environment.data
    req.requestedby = form.requestedby.data
    req.swp_number = form.swp_number.data
    req.version = str(form.swp_number.data).split()[0]
    req.zones = form.zones.data    
    req.start_date = form.start_date.data
    req.delivery_date = form.delivery_date.data
    req.backup_db = form.backup_db.data
    req.keep_data = form.keep_data.data
    req.keep_ld = form.keep_ld.data
    req.osb_integration = form.osb_integration.data
    req.ods_integration = form.ods_integration.data
    req.oss_integration = form.oss_integration.data                        
    req.source_uat_ref = str(form.source_uat_ref.data)
    req.delivery_notification = form.delivery_notification.data 
    req.approval = False
    if new:
        current_session=db_session.object_session(req)
        current_session.add(req)
        current_session.commit()
    else:
        db_session.add(req)
        db_session.commit()

if __name__ == '__main__':
    app.run()

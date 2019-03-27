# models.py

from app import db
from app import admin
from flask_admin.contrib.sqla import ModelView
from wtforms.ext.sqlalchemy.orm import model_form
from flask_security import RoleMixin, UserMixin, current_user
from wtforms.fields import PasswordField

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

envs_requests = db.Table(
    'envs_requests',
    db.Column('env_id', db.Integer(), db.ForeignKey('environment.id')),
    db.Column('req_id', db.Integer(), db.ForeignKey('request.id'))
)

versions_swps = db.Table(
    'versions_swps',
    db.Column('version_id', db.Integer(), db.ForeignKey('version.id')),
    db.Column('swp_id', db.Integer(), db.ForeignKey('swpnumber.id'))
)


class Version(db.Model):
    """"""
    __tablename__ = "version"
    id = db.Column(db.Integer(), primary_key=True)
    version_number = db.Column(db.Integer())

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{}".format(self.version_number)

admin.add_view(ModelView(Version, db.session))


class SwpNumber(db.Model):
    """"""
    __tablename__ = "swpnumber"
    id = db.Column(db.Integer(), primary_key=True)
    version_id = db.Column(db.Integer(), db.ForeignKey("version.id"))
    version = db.relationship("Version", backref=db.backref("version"), order_by=id, lazy=True)
    number= db.Column(db.Integer)

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{} {}".format(self.version, self.number)

admin.add_view(ModelView(SwpNumber, db.session))


class DevelopmentPhase(db.Model):
    """"""
    __tablename__ = "developmentphase"
    id = db.Column(db.Integer(), primary_key=True)
    phase = db.Column(db.String(3))

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{}".format(self.phase)

admin.add_view(ModelView(DevelopmentPhase, db.session))


class Environment(db.Model):
    """"""
    __tablename__ = "environment"
    id = db.Column(db.Integer(), primary_key=True)
    phase_id = db.Column(db.Integer(), db.ForeignKey("developmentphase.id"))
    phase = db.relationship("DevelopmentPhase", backref=db.backref("developmentphase"), order_by=id, lazy=True)
    number = db.Column(db.Integer())

    def __repr__(self):
        #return "{} {}".format(self.phase, self.number)
        return "{}".format(self.id)

    def __str__(self):
        return "{} {}".format(self.phase, self.number)
        #return "{}".format(self.id)

admin.add_view(ModelView(Environment, db.session))


class OsbIntegration(db.Model):
    __tablename__ = "osb_integration"
    id = db.Column(db.Integer(), primary_key=True)
    osbstack = db.Column(db.String(20), unique=True)
    osbstack_ip = db.Column(db.String(20))

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{}".format(self.osbstack)

admin.add_view(ModelView(OsbIntegration, db.session))


class OdsIntegration(db.Model):
    __tablename__ = "ods_integration"
    id = db.Column(db.Integer(), primary_key=True)
    odsnumber = db.Column(db.Integer(), unique=True)

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{}".format(self.odsnumber)

admin.add_view(ModelView(OdsIntegration, db.session))


class OssIntegration(db.Model):
    __tablename__ = "oss_integration"
    id = db.Column(db.Integer(), primary_key=True)
    ossnumber = db.Column(db.Integer(), unique=True)
    ossworkaccount = db.Column(db.String(20))
    osshost = db.Column(db.String(20))

    def __repr__(self):
        return "{}".format(self.id)

    def __str__(self):
        return "{}".format(self.ossnumber)

admin.add_view(ModelView(OssIntegration, db.session))


class EnvironmentRequest(db.Model):
    """"""
    __tablename__ = "request"

    id = db.Column(db.Integer(), primary_key=True)
    environment_id = db.Column(db.Integer(), db.ForeignKey("environment.id"))
    environment = db.relationship("Environment", backref=db.backref("environment"), order_by=id, lazy=True)
    requestedby = db.Column(db.String(20))
    approval = db.Column(db.Boolean())
    status = db.Column(db.String(10))
    zones = db.Column(db.Integer())
    version = db.Column(db.Integer())
    swp_number_id = db.Column(db.Integer(), db.ForeignKey("swpnumber.id"))
    swp_number = db.relationship("SwpNumber", backref=db.backref("swpnumber"), order_by=id, lazy=True)
    start_date = db.Column(db.String())
    delivery_date = db.Column(db.String())
    backup_db = db.Column(db.Boolean())
    keep_data = db.Column(db.Boolean())
    keep_ld = db.Column(db.Boolean())
    osb_id = db.Column(db.Integer(), db.ForeignKey("osb_integration.id"))
    osb_integration = db.relationship("OsbIntegration", backref=db.backref("osb_integration"), order_by=id, lazy=True)
    ods_id = db.Column(db.Integer(), db.ForeignKey("ods_integration.id"))
    ods_integration = db.relationship("OdsIntegration", backref=db.backref("ods_integration"), order_by=id, lazy=True)
    oss_id = db.Column(db.Integer(), db.ForeignKey("oss_integration.id"))   
    oss_integration = db.relationship("OssIntegration", backref=db.backref("oss_integration"), order_by=id, lazy=True)
    source_uat_ref = db.Column(db.String(10), nullable=True)
    delivery_notification = db.Column(db.String(300))

admin.add_view(ModelView(EnvironmentRequest, db.session))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# Customized User model for SQL-Admin
class UserAdmin(ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

admin.add_view(RoleAdmin(Role, db.session)) 
admin.add_view(UserAdmin(User, db.session))
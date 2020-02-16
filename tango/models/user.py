"""
User Model

Defines a model for users. This should not contain any more information than
is necessary for the operation of the site.
"""

from tango import db

from werkzeug.security import generate_password_hash, check_password_hash


# Settings table
# This will store key-value pairs which set user level options
settings = db.Table(
    '_user_settings',
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column('setting_key', db.String(10), primary_key=True),
    db.Column('value', db.String(15))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1024), db.ForeignKey("people.email"), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    settings = db.relationship(settings)

    def __repr__(self):
        return "<User [%r]>" % self.email


    def set_password(self, password):
        """
        Set the user's password
        :param string password: The new password.
        """
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        """
        Check if a password string matches the stored password.
        :param string password: Password you want to check.
        :return: bool: True if the password given matches the user's password.
        """
        return check_password_hash(self.password_hash, password)


    @property
    def is_authenticated(self):
        return True


    @property
    def is_active(self):
        return self.is_verified and not self.is_blocked


    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return u"%d" % (self.id,)

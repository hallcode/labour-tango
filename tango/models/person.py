"""
Person Model

Defines a model for volunteers and contacts. These will be linked to any matching
user accounts, but a user account is not required.
"""
import datetime

from tango import db
from sqlalchemy.sql import func


boundaries = db.Table(
    '_person_boundary',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('boundary_id', db.String(9), db.ForeignKey('boundaries.gss_code'), primary_key=True)
)


class Consent(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"), primary_key=True)
    key = db.Column(db.String(10), primary_key=True)
    origin = db.Column(db.String(10), nullable=False)
    obtained_at = db.Column(db.DateTime, nullable=True, server_default=func.now())
    consent_text = db.Column(db.Text, nullable=True)

    def __init__(self, person_id, key, origin, text=None):
        self.person_id = person_id
        self.key = key
        self.origin = origin
        self.consent_text = text


class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=True)
    last_name = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    mobile_tel = db.Column(db.String(13), unique=False, nullable=True)
    post_code = db.Column(db.String(8), unique=False, nullable=True)
    is_member = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="person", uselist=False)

    consents = db.relationship("Consent", backref="person", lazy=True)

    boundaries = db.relationship('Boundary', secondary=boundaries, lazy='subquery',
                            backref=db.backref('people', lazy=True))

    def __init__(self, fname, lname, email, post_code=None, mobile_tel=None):
        self.first_name = fname.capitalize()
        self.last_name = lname.capitalize()
        self.email = email
        self.post_code = post_code
        self.mobile_tel = mobile_tel

    def __repr__(self):
        return "<Person [%s]>" % self.legal_name

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def legal_name(self):
        return "%s, %s" % (self.last_name.capitalize(), self.first_name)

    def check_consent(self, consent_key):
        consent = Consent.query.with_parent(self).filter_by(key=consent_key).first()

        return False if consent is None else True

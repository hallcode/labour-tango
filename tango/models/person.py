"""
Person Model

Defines a model for volunteers and contacts. These will be linked to any matching
user accounts, but a user account is not required.
"""
import datetime, random, hashlib

from flask import render_template
from tango import db
from tango.services.email import send_email
from sqlalchemy.sql import func


boundaries = db.Table(
    '_person_boundary',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('boundary_id', db.String(9), db.ForeignKey('boundaries.gss_code'), primary_key=True)
)


class VerificationCode(db.Model):
    __tablename__ = 'verification_codes'
    hash = db.Column(db.String(150), primary_key=True)
    expires = db.Column(db.DateTime, nullable=False)

    def __init__(self, hash):
        self.hash = hash
        self.expires = datetime.datetime.now() + datetime.timedelta(minutes=4)



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
    is_email_verified = db.Column(db.Boolean, default=False)

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

    @property
    def email_recipient(self):
        if self.full_name == '':
            return self.email

        return "\"%s\", <%s>" % (self.full_name, self.email)

    def check_consent(self, consent_key):
        consent = Consent.query.with_parent(self).filter_by(key=consent_key).one()
        return False if consent is None else True

    def verify(self, code=None):
        old_codes = VerificationCode.query.filter(
            VerificationCode.expires < datetime.datetime.now()
        )

        old_codes.delete(synchronize_session=False)
        db.session.commit()

        code_hash = hashlib.blake2b()
        code_hash.update(bytes(self.email, encoding='utf-8'))

        if code is not None:
            code_hash.update(bytes(code))

            vcode = VerificationCode.query.get(code_hash.hexdigest())

            if vcode is not None:
                db.session.delete(vcode)
                db.session.commit()
                return True
            else:
                return False

        new_code = random.randint(10000,99999)
        code_hash.update(bytes(new_code))
        vcode = VerificationCode(hash=code_hash.hexdigest())

        db.session.add(vcode)
        db.session.commit()

        email_text = render_template(
            'emails/verify_code.txt',
            code = new_code
        )

        email_html = render_template(
            'emails/verify_code.html',
            name = self.first_name,
            code = new_code,
            email = self.email
        )

        send_email(
            to = self.email,
            subject = 'Your verification code',
            type = 'T',
            body_text = email_text,
            body_html = email_html
        )

        return None

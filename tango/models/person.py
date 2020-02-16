"""
Person Model

Defines a model for volunteers and contacts. These will be linked to any matching
user accounts, but a user account is not required.
"""

from tango import db


boundaries = db.Table(
    '_person_boundary',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('boundary_id', db.String(9), db.ForeignKey('boundaries.gss_code'), primary_key=True)
)


class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=True)
    last_name = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    mobile_tel = db.Column(db.String(13), unique=True, nullable=True)
    post_code = db.Column(db.String(8), unique=False, nullable=True)
    is_member = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="person", uselist=False)

    boundaries = db.relationship('Boundary', secondary=boundaries, lazy='subquery',
                            backref=db.backref('people', lazy=True))

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
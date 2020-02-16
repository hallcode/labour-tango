"""
Boundary Model

A Boundary represents an electoral division, ward, constituency or another
area defined by the Office for National Statistics or Boundary Commission.
"""

from tango import db


class Boundary(db.Model):
    __tablename__ = 'boundaries'

    gss_code = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(3))
    suffix = db.Column(db.String(25))
    parent_id = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=True)

    roads = db.relationship('Road', backref=db.backref('boundary', lazy=False), lazy=True)
    events = db.relationship('Event', backref=db.backref('boundary', lazy=False), lazy=True)
    campaigns = db.relationship('Campaign', backref=db.backref('boundary', lazy=False), lazy=True)

    children = db.relationship('Boundary', backref='parent', lazy=False)

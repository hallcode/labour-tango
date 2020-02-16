"""
Campaign model

A campaign is a particular goal or project.
"""

from tango import db


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    boundary_id = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    events = db.relationship('Event', backref='campaign', lazy=True)
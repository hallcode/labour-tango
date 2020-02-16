"""
Team model

This represents a small grouping of people.
"""

from tango import db


members = db.Table(
    '_person_team',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('team_id', db.String(9), db.ForeignKey('teams.id'), primary_key=True),
    db.Column('is_contact', db.Boolean, nullable=False, default=False)
)


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String, nullable=True)
    boundary_id = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=False)

    events = db.relationship('Event', backref='team', lazy=True)

    members = db.relationship('Person', secondary=members, lazy='subquery',
                                backref=db.backref('teams', lazy='subquery'))
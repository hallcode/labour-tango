"""
Event model

Events are any activity that takes place at a certain place and time,
that people can attend.
"""
from datetime import timedelta

from tango import db


attendance = db.Table(
    '_event_attendance',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('did_attend', db.Boolean, nullable=False, default=False)
)


activity = db.Table(
    '_event_activities',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('activity_type', db.String(10), primary_key=True)
)


roads = db.Table(
    '_event_road',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('road_id', db.BigInteger, db.ForeignKey('roads.id'), primary_key=True),
    db.Column('starting_point', db.Boolean, default=False, nullable=False)
)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String, nullable=False)
    boundary_id = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=False)
    team_id = db.Column(db.String(9), db.ForeignKey('teams.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=True)
    description = db.Column(db.Text, nullable=False)
    contacts_made = db.Column(db.Integer, nullable=True)

    attendees = db.relationship('Person', secondary=attendance, lazy='subquery',
                                backref=db.backref('events', lazy=True))

    roads = db.relationship('Road', secondary=roads, lazy=True,
                                backref=db.backref('events', lazy=True))

    def __repr__(self):
        return "<Event [%r:%s]>" % self.id, self.type

    @property
    def duration(self):
        if self.end_time is None:
            return 0

        duration = self.end_time - self.start_time

        return duration / timedelta(hours=1)
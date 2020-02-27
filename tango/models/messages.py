"""
Messages

Defines the tables for the message queue.
"""
from tango import db


STATUS = {
    " ": "pending",
    "D": "delivered",
    "E": "error",
    "R": "awaiting retry"
}


message_queue = db.Table(
    'message_queue',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('to', db.String(1024), nullable=False),
    db.Column('method', db.String(6), nullable=False, default='EMAIL'),
    db.Column('priority', db.Integer, nullable=False, default=0),
    db.Column('type', db.String(10), nullable=False),
    db.Column('status', db.String(1), nullable=True),
    db.Column('attempts', db.Integer, nullable=True),
    db.Column('body_text', db.Text, nullable=False),
    db.Column('body_html', db.Text, nullable=True),
    db.Column('hold_until', db.DateTime, nullable=True),
    db.Column('expires_on', db.DateTime, nullable=True)
)


exclusion_list = db.Table(
    'recipient_exclusion_list',
    db.Column('hash', db.String(1024), primary_key=True),
    db.Column('until', db.DateTime, nullable=True)
)
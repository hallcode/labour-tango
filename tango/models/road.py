"""
Road model

A road is a named street or thoroughfare as defined by Ordnance Survey.
"""

from tango import db

class Road(db.Model):
    __tablename__ = 'roads'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    boundary_code = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=True)

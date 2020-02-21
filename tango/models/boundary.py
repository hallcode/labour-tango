"""
Boundary Model

A Boundary represents an electoral division, ward, constituency or another
area defined by the Office for National Statistics or Boundary Commission.
"""

from tango import db


class BoundaryType(db.Model):
    __tablename__ = '_boundary_types'

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(100))
    short_name = db.Column(db.String(100), nullable=True)
    abbreviation = db.Column(db.String(10))

    boundaries = db.relationship('Boundary', backref='type', lazy=False)


class Boundary(db.Model):
    __tablename__ = 'boundaries'

    gss_code = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(150))
    type_code = db.Column(db.String(10), db.ForeignKey('_boundary_types.code'))
    parent_id = db.Column(db.String(9), db.ForeignKey('boundaries.gss_code'), nullable=True)

    roads = db.relationship('Road', backref=db.backref('boundary', lazy=False), lazy=True)
    events = db.relationship('Event', backref=db.backref('boundary', lazy=False), lazy=True)
    campaigns = db.relationship('Campaign', backref=db.backref('boundary', lazy=False), lazy=True)

    children = db.relationship('Boundary', backref=db.backref('parent', remote_side=[gss_code]), lazy=False)


    def __repr__(self):
        return '<Boundary [%s:%s]>' % self.type.abbreviation, self.name


    def __init__(self, code, name, parent=None):
        self.gss_code = code
        self.name = name
        self.type_code = code[0:3]

        if parent is not None:
            self.parent_id = parent
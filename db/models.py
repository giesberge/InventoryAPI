from .database import Column, Model, SurrogatePK, db, \
    reference_col, relationship
from apistar import Route
from sqlalchemy import event

from .meta import Base

class Manufacturer(SurrogatePK, Model):
    __tablename__ = 'manufacturer'
    name = Column(db.String(255))
    instruments = relationship('Instrument', backref='manufacturer')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Manufacturer: {}".format(self.name)


class Instrument(SurrogatePK, Model):
    __tablename__ = 'instrument'
    model_name = Column(db.String(255))
    manufacturer_id = reference_col('manufacturer', nullable=True)
    # manufacturer = relationship('Manufacturer', backref='instruments', lazy=False)

    def __init__(self, model_name):
        self.model_name = model_name

    def __repr__(self):
        return "{}".format(self.model_name)


class Measurement(SurrogatePK, Model):
    __tablename__ = 'measurement'
    name = Column(db.String(255))

    def __init__(self, name):
        self.name = name


class MeasurementAssociation(SurrogatePK, Model):
    __tablename__ = 'measurementassocation'
    instrument_id = reference_col('instrument', nullable=False)
    instrument = relationship('Instrument', backref='measurement')
    measurement_id = reference_col('measurement', nullable=False)
    measurement = relationship('Measurement')
    range_min = Column(db.Float)
    range_max = Column(db.Float)
    accuracy = Column(db.Float)
    precision = Column(db.Float)
    notes = Column(db.Text)
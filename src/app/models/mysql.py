# -*- coding: utf-8 -*-
from app.database import db
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Numeric
from sqlalchemy.ext.declarative import declarative_base
from app.utils import get_openid_user

Base = declarative_base()

from opentelemetry import trace
tracer = trace.get_tracer(__name__)

import traceback, logging
logger = logging.getLogger(__name__)


class Fakenames(Base):

    __tablename__ = 'fakenames'

    number = Column(Integer, primary_key=True, unique=True)
    gender = Column(String(6))
    nameset = Column(String(25))
    title = Column(String(6))
    givenname = Column(String(20))
    middleinitial = Column(String(1))
    surname = Column(String(23))
    streetaddress = Column(String(100))
    city = Column(String(100))
    state = Column(String(22))
    statefull = Column(String(100))
    zipcode = Column(String(15))
    country = Column(String(2))
    countryfull = Column(String(100))
    emailaddress = Column(String(100))
    username = Column(String(25))
    password = Column(String(25))
    browseruseragent = Column(String(255))
    telephonenumber = Column(String(25))
    telephonecountrycode = Column(Integer)
    mothersmaiden = Column(String(23))
    birthday = Column(DateTime)
    age = Column(Integer)
    tropicalzodiac = Column(String(11))
    cctype = Column(String(10))
    ccnumber = Column(String(16))
    cvv2 =  Column(Integer)
    ccexpires = Column(String(10))
    nationalid = Column(String(20))
    ups = Column(String(24))
    westernunionmtcn = Column(String(10))
    moneygrammtcn = Column(String(8))
    color = Column(String(6))
    occupation = Column(String(70))
    company = Column(String(70))
    vehicle = Column(String(255))
    domain = Column(String(70))
    bloodtype = Column(String(3))
    pounds = Column(Numeric(5,1))
    kilograms = Column(Numeric(5, 1))
    feetinches = Column(String(6))
    centimeters = Column(SmallInteger)
    guid = Column(String(36))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))

    # Explicit SQLAlchemy class constructor
    def __init__(self, **kwargs):
        super(Fakenames, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Number {self.number}>, <GUID {self.guid}>'

    @property
    def serialize(self):
        return {
            'number': self.number,
            'gender': self.gender,
            'nameset': self.nameset,
            'title': self.title,
            'givenname': self.givenname,
            'middleinitial': self.middleinitial,
            'surname': self.surname,
            'streetaddress': self.streetaddress,
            'city': self.city,
            'state': self.state,
            'statefull': self.statefull,
            'zipcode': self.zipcode,
            'country': self.country,
            'countryfull': self.countryfull,
            'emailaddress': self.emailaddress,
            'username': self.username,
            'password': self.password,
            'browseruseragent': self.browseruseragent,
            'telephonenumber': self.telephonenumber,
            'telephonecountrycode': self.telephonecountrycode,
            'mothersmaiden': self.mothersmaiden,
            'birthday': self.birthday,
            'age': self.age,
            'tropicalzodiac': self.tropicalzodiac,
            'cctype': self.cctype,
            'ccnumber': self.ccnumber,
            'cvv2': self.cvv2,
            'ccexpires': self.ccexpires,
            'nationalid': self.nationalid,
            'ups': self.ups,
            'westernunionmtcn': self.westernunionmtcn,
            'moneygrammtcn': self.moneygrammtcn,
            'color': self.color,
            'occupation': self.occupation,
            'company': self.company,
            'vehicle': self.vehicle,
            'domain': self.domain,
            'bloodtype': self.bloodtype,
            'pounds': self.pounds,
            'kilograms': self.kilograms,
            'feetinches': self.feetinches,
            'centimeters': self.centimeters,
            'guid': self.guid,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def create(self) -> bool:
        """ Creates a database entry """
        response = True

        try:
            with tracer.start_as_current_span(name='create'):
                current_span = trace.get_current_span()
                current_span.set_attributes({'enduser.id': get_openid_user()})

                db.session.add(self)
                db.session.commit()

                logger.info(f'Creating row "{self.guid}" succeeded!')
                status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Creating row failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False
        current_span.set_status(status)
        return False if response == False else True

    def read_all() -> list:
        """ Retreive all records from the table """
        try:
            with tracer.start_as_current_span(name='get_all'):
                current_span = trace.get_current_span()
                current_span.set_attributes({'enduser.id': get_openid_user()})

                response = db.session.query(Fakenames).all()
                status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = e
        current_span.set_status(status)
        return response

    def read(guid) -> list:
        """ Retrieve a given identity"""
        try:
            with tracer.start_as_current_span(name='get'):
                current_span = trace.get_current_span()
                current_span.set_attributes({'enduser.id': get_openid_user()})

                response = db.session.query(Fakenames).filter(Fakenames.guid == guid).limit(1).all()
                response = response[0]

                status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = e
        current_span.set_status(status)
        return response

    def udpate(self) -> bool:
        """ Creates a database entry """
        response = True

        try:
            with tracer.start_as_current_span(name='update'):
                current_span = trace.get_current_span()
                current_span.set_attributes({'enduser.id': get_openid_user()})

                db.session.merge(self)
                db.session.commit()

                status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False
        current_span.set_status(status)
        return False if response == False else True

    def delete(self) -> bool:
        """ Deletes a database entry """
        response =  True

        try:
            with tracer.start_as_current_span(name='delete'):
                current_span = trace.get_current_span()
                current_span.set_attributes({'enduser.id': get_openid_user()})

                db.session.delete(self)
                db.session.commit()

                status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            status = trace.status.Status(trace.StatusCode.ERROR)
            current_span.record_exception(e)
            response = False
        current_span.set_status(status)
        return False if response == False else True

# -*- coding: utf-8 -*-
from mvc_flask_dash.database import db

from sqlalchemy.ext.declarative import declarative_base
from mvc_flask_dash.utils import get_openid_user

Base = declarative_base()

from opentelemetry import trace
tracer = trace.get_tracer(__name__)

import traceback, logging
logger = logging.getLogger(__name__)


class Fakenames(Base):
    
    __tablename__ = 'fakenames'
    
    number = db.Column(db.Integer, primary_key=True, unique=True)
    gender = db.Column(db.String(6))
    nameset = db.Column(db.String(25))
    title = db.Column(db.String(6))
    givenname = db.Column(db.String(20))
    middleinitial = db.Column(db.String(1))
    surname = db.Column(db.String(23))
    streetaddress = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(22))
    statefull = db.Column(db.String(100))
    zipcode = db.Column(db.String(15))
    country = db.Column(db.String(2))
    countryfull = db.Column(db.String(100))
    emailaddress = db.Column(db.String(100))
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))
    browseruseragent = db.Column(db.String(255))
    telephonenumber = db.Column(db.String(25))
    telephonecountrycode = db.Column(db.Integer)
    mothersmaiden = db.Column(db.String(23))
    birthday = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    tropicalzodiac = db.Column(db.String(11))
    cctype = db.Column(db.String(10))
    ccnumber = db.Column(db.String(16))
    cvv2 =  db.Column(db.Integer)
    ccexpires = db.Column(db.String(10))
    nationalid = db.Column(db.String(20))
    ups = db.Column(db.String(24))
    westernunionmtcn = db.Column(db.String(10))
    moneygrammtcn = db.Column(db.String(8))
    color = db.Column(db.String(6))
    occupation = db.Column(db.String(70))
    company = db.Column(db.String(70))
    vehicle = db.Column(db.String(255))
    domain = db.Column(db.String(70))
    bloodtype = db.Column(db.String(3))
    pounds = db.Column(db.Numeric(5,1))
    kilograms = db.Column(db.Numeric(5,1))
    feetinches = db.Column(db.String(6))
    centimeters = db.Column(db.SmallInteger)
    guid = db.Column(db.String(36))
    latitude = db.Column(db.Numeric(10,8))
    longitude = db.Column(db.Numeric(11,8))


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
        response =  True
        
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
        response =  True
        
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
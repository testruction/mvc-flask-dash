# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('./src/')

import typing
import sqlalchemy

import pytest
from flask import Flask
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy

from mvc_flask_dash.models.postgres import db, Base

@pytest.fixture
def app(request: pytest.FixtureRequest) -> Flask:
    app = Flask(request.module.__name__)
    import mvc_flask_dash.config as config
    app.config.from_object(config.DevelopmentConfig)
    return app


@pytest.fixture
def app_ctx(app: Flask) -> typing.Generator[AppContext, None, None]:
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def db(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app)


@pytest.fixture
def tables(app: Flask, db: SQLAlchemy) -> typing.Any:    
    connection = db.engine.connect()
    Base.metadata.bind = connection

    with app.app_context():
        Base.metadata.create_all()

    yield

    with app.app_context():
        Base.metadata.drop_all()

@pytest.fixture
def dbsession(db, tables):
    from sqlalchemy.orm import Session
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = db.engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()

# @pytest.fixture(scope='session')
# def app():
#     from flask import Flask
#     app = Flask(__name__)
    
#     from mvc_flask_dash.config import DevelopmentConfig
#     app.config.from_object(DevelopmentConfig)
    
#     from flask_sqlalchemy import SQLAlchemy
#     db = SQLAlchemy(app) # Database Initialization
    
#     app.app_context().push()
    
#     yield app

    
# @pytest.fixture(scope='function')
# def dbsession(app):
#     db.init_app(app)
    
#     connection = db.engine.connect()
#     transaction = connection.begin()
    
#     Base.metadata.bind = connection
#     Base.metadata.create_all()
    
#     yield db.session
    
#     transaction.close()
#     Base.metadata.drop_all()

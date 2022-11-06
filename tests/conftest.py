# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('./src/')

import typing as t

import pytest
from flask import Flask
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from project.config import DevelopmentConfig

import logging
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger.setLevel('DEBUG')

from project.models.postgres import Fakenames, Base

import pkg_resources
dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')


# def pytest_sessionstart(session):
#     engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
#     Base.metadata.create_all(engine)

#     def lower_first(iterator):
#         import itertools
#         return itertools.chain([next(iterator).lower()], iterator)

#     import csv
#     from contextlib import closing
#     with Session(bind=engine) as session:
#         with closing(open(dataset, encoding='utf-8-sig')) as f:
#             reader = csv.DictReader(lower_first(f))

#             for row in reader:
#                 session.add(Fakenames(**row))
#         session.commit()
#         session.close()

@pytest.fixture
def app(request: pytest.FixtureRequest) -> Flask:
    app = Flask(request.module.__name__)
    app.config.from_object(DevelopmentConfig)
    return app


@pytest.fixture
def app_ctx(app: Flask) -> t.Generator[AppContext, None, None]:
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def db(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app, model_class=Fakenames)


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def tables(app: Flask, db: SQLAlchemy) -> t.Any:    
    Base.metadata.bind = db.engine.connect()
    Base.metadata.create_all(db.engine)
    # db.create_all()

    import itertools
    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    import csv
    from contextlib import closing
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        
        for row in reader:
            db.session.add(Fakenames(**row))
        db.session.commit()

    yield Fakenames

    Base.metadata.drop_all()
    # db.drop_all()
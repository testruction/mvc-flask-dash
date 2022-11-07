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

from project.models.postgres import Fakenames, Base
from project.models.postgres import db as _db

import pkg_resources
dataset = pkg_resources.resource_filename(__name__,
                                          'integration/fakenames.csv')


def pytest_sessionstart(session):
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

    def lower_first(iterator):
        import itertools
        return itertools.chain([next(iterator).lower()], iterator)

    import csv
    from contextlib import closing
    with Session(bind=engine) as session:
        with closing(open(dataset, encoding='utf-8-sig')) as f:
            reader = csv.DictReader(lower_first(f))

            for row in reader:
                session.add(Fakenames(**row))
        session.commit()
        session.close()


def pytest_unconfigure():
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)


@pytest.fixture
def app(request: pytest.FixtureRequest) -> Flask:
    app = Flask(request.module.__name__)
    app.config.from_object(DevelopmentConfig)
    _db.init_app(app)
    return app


@pytest.fixture
def app_ctx(app: Flask) -> t.Generator[AppContext, None, None]:
    with app.app_context() as ctx:
        yield ctx

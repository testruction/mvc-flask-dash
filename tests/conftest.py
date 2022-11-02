# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
sys.path.append('./src/')

import typing as t

import pytest
from flask import Flask
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy

from app.models.postgres import Fakenames, db, Base

@pytest.fixture
def app(request: pytest.FixtureRequest) -> Flask:
    app = Flask(request.module.__name__)
    import app.config as config
    app.config.from_object(config.DevelopmentConfig)
    
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
    
    db.create_all()

    yield

    db.drop_all()
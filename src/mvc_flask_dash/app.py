# -*- coding: utf-8 -*-
from flask import Flask
from flasgger import Swagger
from flask_assets import Environment

from opentelemetry.instrumentation.flask import FlaskInstrumentor

import mvc_flask_dash.config as config
from mvc_flask_dash.database import create_db, get_migrate
from mvc_flask_dash.controllers.postgres import postgres_controllers
from mvc_flask_dash.views.index import index_views
from mvc_flask_dash.views.dashboards.postgres import init_postgres_dashboard
# New views must be imported and added to this list
views = [index_views,
         postgres_controllers]

def add_views(flask_server, views):
    """ register views """
    for view in views:
        flask_server.register_blueprint(view)

def add_swagger(flask_server):
    flask_server.config["SWAGGER"] = {
        "swagger_version": "2.0",
        "title": "Application",
        "specs": [
            {
                "version": "0.0.1",
                "title": "Application",
                "endpoint": "spec",
                "route": "/apis/spec",
                "rule_filter": lambda rule: True,  # all in
            }
        ],
        "static_url_path": "/apidocs",
    }

    Swagger(flask_server)


def create_app():
    """
    Web application initialization
    """
    app = Flask(__name__,
                static_folder='static',
                instance_relative_config=False)
    app.config.from_object(config.ProductionConfig)
    
    
    # Enable flask telemetry
    from opentelemetry import trace
    from mvc_flask_dash.utils import get_openid_user
    def request_hook(span: trace.get_current_span(), environ: app.wsgi_app):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user())
    FlaskInstrumentor().instrument_app(app,
                                       request_hook=request_hook,
                                       excluded_urls="health",
                                       enable_commenter=True)

    assets = Environment()
    assets.init_app(app)
    create_db(app)
    
    # Import views
    with app.app_context():
        add_views(flask_server=app, views=views)
        init_postgres_dashboard(flask_server=app)
        add_swagger(flask_server=app)
        
        return app


server = create_app()
migrate = get_migrate(server)

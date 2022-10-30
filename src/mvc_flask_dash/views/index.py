# -*- coding: utf-8 -*-
import pkg_resources, pathlib
from flask import Blueprint, render_template

TEMPLATE = pkg_resources.resource_filename(__name__, 'templates/index.html.j2')

index_views = Blueprint('index',
                        __name__,
                        template_folder=pathlib.Path(TEMPLATE).parent.as_posix())

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template(pathlib.Path(TEMPLATE).name)

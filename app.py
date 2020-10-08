import os
import subprocess

from flask import Flask, render_template, url_for, make_response, request, jsonify
from werkzeug.utils import secure_filename

import keyboard

from hotgrid import HotGrid
from hotgrid.actions import HotGridAction, HotGridActionKeyboard, HotGridActionOpenProcess

UPLOAD_FOLDER = 'static/icons'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

hotgrid = HotGrid()
hotgrid.add('volume up', action=HotGridActionKeyboard('volume up'))
hotgrid.add('volume down', action=HotGridActionKeyboard('volume down'))
hotgrid.add('open spotify', icon_image="sppogify.png", action=HotGridActionOpenProcess('spotify'))
hotgrid.add('refresh page', action=HotGridActionKeyboard('f5'))

@app.route('/')
def hello_world():
    return render_template(
        'hotgrid.j2', 
        hotgrid=hotgrid.get_hotgrid(), 
        hotgrid_actions=hotgrid.get_actions(),
        hotgrid_action_fields=hotgrid.get_config_items()
    )

@app.route('/activate/<int:grid_index>', methods=['POST'])
def activate_hotgrid(grid_index):
    if grid_index < 0 or grid_index > hotgrid.grid_size:
        return { 'error': 'Invalid index', 'status': 500 }
    hotgrid.activate(grid_index)
    return { 'status': 200 }

@app.route('/config', methods=['POST'])
def configure_hotgrid():
    json_data = request.get_json()
    grid_element = hotgrid.get_hotgrid()[json_data['element'] - 1]
    action = HotGridAction.subclasses[json_data['action'] - 1](json_data['fields'][0]['value'])
    grid_element.action = action
    hotgrid.modify_element(grid_element, json_data['element'] - 1)

    return {'status': 200}

import os
import subprocess

from flask import Flask, render_template, url_for, make_response, \
    request, jsonify, send_from_directory, flash
from werkzeug.utils import secure_filename

import keyboard

from hotgrid import HotGrid
from hotgrid.actions import HotGridAction, HotGridActionKeyboard, HotGridActionOpenProcess

ICON_FOLDER = './icons'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['ICON_FOLDER'] = ICON_FOLDER

hotgrid = HotGrid()


@app.route('/')
def hotgrid_home():
    return render_template(
        'hotgrid.j2', 
        hotgrid=hotgrid.get_hotgrid(), 
        hotgrid_actions=hotgrid.get_actions(),
        hotgrid_action_fields=hotgrid.get_config_items()
    )


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_icon(file):
    if file.filename == '':
        return {'status': 500, 'error': 'No selected file.'}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        icon_url = os.path.join(app.config['ICON_FOLDER'], filename)
        file.save(icon_url)
        return {'status': 200, 'icon_image': filename}
        

@app.route('/api/hotgrid/icon', methods=['GET', 'POST'])
def hotgrind_icon():
    if request.method == 'POST':
        if 'file' in request.files:
            return upload_icon(request.files['file'])
    elif request.method == 'GET':
        data = request.get_json()
        if data:
            index = data['element']
            element_icon = hotgrid.get_icon(index)
            return {'status': 200, 'icon_image': icon_url}
    return {'status': 500, 'error': 'Invalid request.'}
        
@app.route('/icons/<filename>')
def get_icon(filename):
    return send_from_directory(app.config['ICON_FOLDER'], filename)


@app.route('/api/hotgrid', methods=['POST'])
def hotgrid_api():
    data = request.get_json()
    if not data:
        return {'status': 500, 'error': 'No JSON data specified.'}

    grid_index = data['element']
    if 'active' in data.keys():
        grid_state = data['active']
        hotgrid.activate(grid_index)
    elif 'icon_image' in data.keys():
        grid_icon_image = data['icon_image']
        hotgrid.set_icon(grid_index, grid_icon_image)

    return { 
        'element': grid_index, 
        'active': hotgrid.is_active(grid_index), 
        'icon_image': hotgrid.get_hotgrid()[grid_index].icon_image,
        'status': 200 
    }


@app.route('/api/config', methods=['POST'])
def configure_hotgrid():
    data = request.get_json()
    if not data:
        return {'status': 500, 'error': 'No JSON data specified.'}
    grid_index =  data['element']
    grid_action = data['action']

    if grid_index < 0 or grid_index > hotgrid.grid_size:
        return {'status': 500, 'error': 'Index out of range.'}

    grid_element = hotgrid.get_hotgrid()[grid_index]
    action = HotGridAction.subclasses[grid_action](data['fields'][0]['value'])
    grid_element.action = action
    grid_element.enabled = True

    hotgrid.modify_element(grid_element, grid_index)

    return {
        'element': grid_index,
        'enabled': grid_element.enabled,
        'status': 200
    }

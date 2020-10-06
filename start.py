from flask import Flask, render_template, url_for, make_response, request
import keyboard
import subprocess

from hotgrid import HotGrid
from hotgrid.actions import HotGridActionKeyboard, HotGridActionOpenProcess

app = Flask(__name__)

hotgrid = HotGrid()
hotgrid.add('volume up', 'test_icon.png', HotGridActionKeyboard('volume up'))
hotgrid.add('volume down', 'test_icon.png', HotGridActionKeyboard('volume down'))
hotgrid.add('open spotify', 'test_icon.png', HotGridActionOpenProcess('spotify'))
hotgrid.add('refresh page', 'test_icon.png', HotGridActionKeyboard('f5'))
hotgrid.add('type woohoo python', 'test_icon.png', HotGridActionKeyboard('oh boy I love python!', write=True))

@app.route('/')
def hello_world():
    return render_template('hotgrid.j2', tiles=hotgrid.get_hotgrid())

@app.route('/activate/<int:grid_index>', methods=['POST'])
def activate_hotgrid(grid_index):
    if grid_index < 0 or grid_index > hotgrid.grid_size:
        return { 'error': 'Invalid index', 'status': 500 }
    hotgrid.activate(grid_index)
    return { 'status': 200 }

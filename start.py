from flask import Flask, render_template, url_for, make_response, request

from .hotgrid import HotGridElement

import keyboard

app = Flask(__name__)

images = [
        HotGridElement('volume up',  'test_icon.png', lambda: keyboard.send('volume up')),
        HotGridElement('volume down',  'test_icon.png', lambda: keyboard.send('volume down')),
        HotGridElement('refresh page','test_icon.png', lambda: keyboard.send('f5')),
]

@app.route('/')
def hello_world():
    return render_template('hotgrid.j2', tiles=images)

@app.route('/activate/<int:grid_index>', methods=['POST'])
def activate_hotgrid(grid_index):
    images[grid_index].activate()
    return { 'status': 200 }

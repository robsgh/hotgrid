# HotGrid
A fully-responsive productivity companion accessible from anywhere with a browser!

Transform an old tablet or phone into a convenient one-touch tool to easily control your computer.

## What can HotGrid do right now?
HotGrid allows you to customize any amount of HotGrid elements to perform actions on your computer.
Currently, keyboard macros and opening programs is supported. The action system is designed with
customization in mind. This means that if you have an idea or integration you would like to add,
doing so should be relatively painless.

Python was chosen as HotGrid's language because it has a wide variety of SDK's and bindings
for users to use.

This means the following could be possible with HotGrid:
* REST calls to a weather API to change the icon based on current conditions
* Remotely reboot a router by tapping a HotGrid
* Full interface automation through PyGame
* Integrate with OBS Websockets API to change scenes easily 

## Usage Instructions
_WARNING: HotGrid is under heavy development! Use at your own risk!_

Setting up HotGrid is fairly simple!
1. Clone the git repository to the machine you want to control
2. Setup a python3 venv to use for HotGrid
3. Install the requirements
> `pip install -r requirements.txt`
4. Run flask
> `flask run --host 0.0.0.0` in the repo root folder
5. Navigate to `http://yourcomputerip:5000/` on your tablet or phone
6. Enjoy HotGrid!

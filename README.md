# LAN Game Scanner

This is a modular approach to scan for gameservers on local networks e.g. LAN-Parties.

Since this is currently contains first tests no further documentations is currently available but will be added later.

The goal is to scan a network and find gameservers for example CSGO, Call Of Duty and Team Fortress 2. All found servers are then saved to a file for further evaluation and to display them e.g. by some kind of web frontend.

The scanner should be easily configurable and expandable to support many different servers, games and protocols.

In theory this scanner could also scan online IP Adresses.

## Install instuctions

Download the repository
```
git clone https://github.com/991jo/lan-game-scanner.git 
```
then you probably want to make a python virtualenv with python3. Take care, the name of the command might be slightly different on some systems.
```
virtualenv lan-game-scanner
```
Now install the the requirements
```
cd lan-game-scanner
pip install -r requirements.txt
```
Now you can add your IPs in src/run.py


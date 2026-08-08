from flask import Flask, render_template
import json
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # test for playtime thing, how can one have a input username? Convert to uuid and compare to files in \stats\, if non say player not found or something.
    with open(r'C:\STUFF2123123\Minecraft SErver Vanilla\world\players\stats\0b2ea760-705e-4737-81c8-2df33aea959a.json', 'r') as f:
        datastats = json.load(f)
    playtime = datastats['stats']['minecraft:custom']['minecraft:play_time']
    hours = playtime // 72000

    #API for server stuff, true/false.
    externalresponse = requests.get('https://api.mcstatus.io/v2/status/java/supergood.work.gd').json()
    onlinestatus = externalresponse['online'] # T/F
    players = externalresponse['players']['online']

    return render_template('index.html', onlinestatus = onlinestatus, PThours = hours, players=players)

if __name__ == '__main__':
    app.run()
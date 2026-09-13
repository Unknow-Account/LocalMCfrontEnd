# Set up stuff

ServerIP = "mc.justawebsite.cc"
Stats_Folder = r'C:\STUFF2123123\Minecraft SErver Vanilla\world\players\stats'

#

UUIDUser = 0

from flask import Flask, render_template, request, jsonify
import json
import os
import requests
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    # API for server things and yeah
    externalresponse = requests.get(f"https://api.mcstatus.io/v2/status/java/{ServerIP}").json()

    onlinestatus = externalresponse['online']
    players = externalresponse.get('players', {}).get('online', 0)

    if onlinestatus:
        onlinestatus = "online"
    else:
        onlinestatus = "offline"

    return render_template('index.html', SERVER=ServerIP,onlinestatus=onlinestatus,PThours="N/A",players=players)


@app.route('/get-data', methods=['POST'])
def get_data():
    data = request.get_json()
    user_name = data.get('userInput')

    if not user_name:
        return jsonify({'success': False,
                        'output': 'Enter A Username'})

    ## UUID API
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user_name}")

    api_response = response.json()

    print(api_response)

    ## BEDROCK API 
    def Bedrock_Uuid_Api(UserName):
        response = requests.get(f"https://mc-api.io/profile/{UserName}/BEDROCK")
        api_response = response.json()

        if (api_response.get('uuid')):
            UUIDUser = str(uuid.UUID(api_response['uuid']))
        else:
            UUIDUser = str(uuid.UUID(int=0))

        return UUIDUser
    ## End of BEDROCK API

#

    if (api_response.get('errorMessage')):
        UUIDUser = Bedrock_Uuid_Api(user_name)
    else:
        UUIDUser = str(uuid.UUID(api_response['id']))

    stats_file = os.path.join(Stats_Folder,f'{UUIDUser}.json')



    # Does player have  stat file whatever thing?
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            datastats = json.load(f)
        playtime = datastats ['stats']['minecraft:custom']['minecraft:play_time']
        hours = playtime // 72000

        player_exist = True

    else:
        hours = "N/A"
        player_exist = False
    print(hours)
    return jsonify ({'success': True,'output': UUIDUser, 'hours': hours, 'player_exist': player_exist,"PThours":hours})



if __name__ == '__main__':
    app.run()
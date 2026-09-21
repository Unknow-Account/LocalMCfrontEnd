# Set up stuff

ServerIP = ""
Stats_Folder = r''

# extra
api_request_timeout = 10 # In seconds
CacheTimeout = 600 # In seconds, for caching server stats api. 60 = save for 60 seconds then request again (if requested)
#

UUIDUser = 0

from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
import json
import os
import requests
import uuid
import re

app = Flask(__name__)
#Caching import stuff config
config = {
    "DEBUG": True,          
    "CACHE_TYPE": "SimpleCache", 
    "CACHE_DEFAULT_TIMEOUT": CacheTimeout
}
app.config.from_mapping(config)
cache = Cache(app)



@cache.cached(key_prefix='shared_api_data')
def api_data():
        # API for server things and yeah
    try:
        externalresponse = requests.get(f"https://api.mcstatus.io/v2/status/java/{ServerIP}", timeout = api_request_timeout).json()
        print("api-pulled-mcstatus(Server Status)")
    except:
        print("mojang-api-timed-out")
        externalresponse = {"online": False}

    onlinestatus = externalresponse['online']
    players1 = externalresponse.get('players', {}).get('online', 0)


    if onlinestatus:
        onlinestatus = "online"
        players=(str(players1) + "people are currently online")
    else:
        onlinestatus = "offline"
        players=" "


    # Temp dont wanna start the server okay
    # onlinestatus = "online"
    # players = "0 people are currently online"


    # Sets server info body to green/red. Only green if online-anything else red.
    ServerStatsBodyColor = "Background-color: rgba(5, 139, 5, 0.5);"
    TitleBGColor = "Background-color: rgba(155, 30, 14, 0.581);"

    if onlinestatus == "online":
        ServerStatsBodyColor = "Background-color: rgba(5, 139, 5, 0.5);"
        TitleBGColor = "Background-color: rgba(30, 155, 14, 0.581)"
    else:
        ServerStatsBodyColor = "Background-color: rgba(139, 5, 5, 0.5);"
        TitleBGColor = "Background-color: rgba(155, 30, 14, 0.581);"




    

    return {"SERVER":ServerIP,"onlinestatus":onlinestatus,"PThours":"N/A","players":players,"ServerStatsBodyColor":ServerStatsBodyColor,"TitleBGColor":TitleBGColor}

@app.route('/')
def index():

    stats_shared = api_data()

    ServerIP=stats_shared["SERVER"]
    onlinestatus=stats_shared["onlinestatus"]
    PThours=stats_shared["PThours"]
    ServerStatsBodyColor=stats_shared["ServerStatsBodyColor"]
    TitleBGColor=stats_shared["TitleBGColor"]
    players=stats_shared["players"]

    return render_template('index.html', SERVER=ServerIP,onlinestatus=onlinestatus,PThours=PThours,players=players, ServerStatsBodyColor=ServerStatsBodyColor, TitleBGColor = TitleBGColor)


@app.route('/get-data', methods=['POST'])
def get_data():
    data = request.get_json()
    user_name = data.get('userInput')
    UserNameCheckList = re.compile(r'^[A-Za-z0-9_]{3,16}$|^[A-Za-z0-9_][A-Za-z0-9_ ]{1,13}[A-Za-z0-9_]$')

    if not user_name:
        return jsonify({'success': False,
                        'output': 'Enter A Username'})
    if not UserNameCheckList.match(user_name):
        return jsonify({'success': False, 'output': 'Not Valid username-Stop trying to hack.'})

    ## UUID API
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user_name}", timeout = api_request_timeout)
        api_response = response.json()
    except:
        print("api-java-timeout")
        response = {'errorMessage': 'Timeout'}
        api_response = response
        
    print("api-pulled-mojang(java)")
    print(api_response)

    ## BEDROCK API 
    def Bedrock_Uuid_Api(UserName):
        try:
            response = requests.get(f"https://mc-api.io/profile/{UserName}/BEDROCK", timeout = api_request_timeout)
            api_response = response.json()
        except:
            print("api-bedrock-timeout")
            response = {'errorMessage': 'Timeout'}
            api_response = response

        print("api-pulled-mc-api(bedrock)")
        print(api_response)
        if (api_response.get('uuid')):
            UUIDUser = str(uuid.UUID(api_response['uuid']))
        else:
            UUIDUser = str(uuid.UUID(int=0))

        return UUIDUser
    ## End of BEDROCK API

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




    return jsonify ({'success': True,'output': UUIDUser, 'hours': hours, 'player_exist': player_exist,"PThours":hours})



@app.route('/Detailed_User_Stats')
def Detailed_User_Stats():

    stats_shared = api_data()

    TitleBGColor = stats_shared['TitleBGColor']


    return render_template('Detailed_User_Stats.html', SERVER = ServerIP, TitleBGColor = TitleBGColor,)

@app.route('/DSU_Type_Send', methods=['POST'])
def DSUTypeSend():
    DropDown = request.form.get('DSU_Type_Choice')
    UserName = request.form.get('Username_DSU')

    print(DropDown)
    print(UserName)

    return jsonify ({'DropDown':DropDown,'UserName':UserName})







if __name__ == '__main__':
    app.run()

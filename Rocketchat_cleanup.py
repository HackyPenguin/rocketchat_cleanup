import requests
import json
from datetime import datetime
import time
import datetime

# must be in rooms you wish to cleanup
user = "your_user"
serverUrl = "https://yourURLHERE/api/v1/"
password = "your_users_password"
#  change the timedelta to point to how long you want to delete from
delete_to = datetime.datetime.utcnow() + datetime.timedelta(-30)

# couldnt format MS way rocketchat wanted it so lazy

delete_to = delete_to.strftime("%Y-%m-%dT%H:%M:%S") + ".304Z"

delete_from = datetime.datetime.utcnow() + datetime.timedelta(-360)
delete_from = delete_from.strftime("%Y-%m-%dT%H:%M:%S") + ".304Z"


def login():
    payload = {
        "username": user,
        "password": password
        }
    loginurl = serverUrl + "login"
    response = requests.post(loginurl, data=payload)
    userid = json.loads(response.text)["data"]["userId"]
    token = json.loads(response.text)["data"]["authToken"]
    auth = {
        "X-User-Id": userid,
        "X-Auth-Token": token
    }
    return auth

token = login()

def getchannels(auth):
    rooms = []
    groupsurl = serverUrl + "channels.list.joined"
    channels = requests.get(groupsurl, headers=auth)
    data = json.loads(channels.text)["channels"]
    for i in data:
        rooms.append(i['_id'])
    return rooms


def channelclean(auth, delete_to, delete_from, roomid):
    channelcleanurl = serverUrl + "channels.cleanHistory"
    payload = {
        "roomId": roomid,
        "latest": delete_to,
        "oldest": delete_from
        }
    r = requests.post(channelcleanurl, headers=auth, data=payload)
    return r


def groupconverter(auth, roomid, type):
    channelchange = serverUrl + "groups.setType"
    payload = {
           "roomId": roomid,
           "type": type
           }
    r = requests.post(channelchange, headers=auth, data=payload)
    return r


def channelconverter(auth, roomid, type):
    channelchange = serverUrl + "channels.setType"
    payload = {
           "roomId": roomid,
           "type": type
          }
    r = requests.post(channelchange, headers=auth, data=payload)
    return r


def getgroups(auth):
    rooms = []
    groupsurl = serverUrl + "groups.list"
    channels = requests.get(groupsurl, headers=auth)
    data = json.loads(channels.text)['groups']
    for i in data:
        rooms.append(i['_id'])
    return rooms

# lets get messages from channels first


rooms = getchannels(token)



rooms = getchannels(token)
for x in rooms:
    print(channelclean(token, delete_to, delete_from, x))

privaterooms = getgroups(token)
for x in privaterooms:
    print(groupconverter(token, x, "c"))
    print(channelclean(token, delete_to, delete_from, x))
    print(channelconverter(token, x, "p"))

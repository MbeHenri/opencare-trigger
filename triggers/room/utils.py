import base64
from datetime import datetime
import requests
from triggers.config import environ


# insertion des utilisateurs dans la base de données du portail des doctors
def insert_user_to_talk(username, display):
    # initialisation
    talk_url = environ["TALK_URL"]
    user = environ["TALK_USER"]
    password = environ["TALK_PASSWORD"]
    talk_base_pwd = environ["TALK_INIT_PASSWORD"]

    TALK_BASE64 = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")

    headers = {
        "Accept": "application/json",
        "OCS-APIRequest": "true",
        "Content-Type": "application/json",
        "Authorization": f"Basic {TALK_BASE64}",
    }

    payload = {
        "userid": username,
        "displayName": display,
        "password": talk_base_pwd,
    }

    response = requests.post(
        f"{talk_url}/ocs/v2.php/cloud/users",
        headers=headers,
        json=payload,
    )

    # print(response.text
    # print(f"{response.text}")
    if response.status_code == 400 or response.ok:
        if response.status_code == 400:
            data = response.json()
            status = data["ocs"]["meta"]["statuscode"]

            if status != 102:
                print(
                    f"[Room] [user] [{datetime.now()}] sync Identifier({username}) error"
                )
            else:
                print(
                    f"[Room] [user] [{datetime.now()}] sync Identifier({username}) exist"
                )
        else:
            print(
                f"[Room] [user] [{datetime.now()}] sync Identifier({username}) created"
            )
    else:
        print(f"[Room] [user] [{datetime.now()}] sync Identifier({username}) error")


def create_room(name):
    # initialisation
    talk_url = environ["TALK_URL"]
    user = environ["TALK_USER"]
    password = environ["TALK_PASSWORD"]
    payload = {"roomType": "2", "roomName": f"{name}"}

    TALK_BASE64 = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")
    headers = {
        "OCS-APIRequest": "true",
        "Accept": "application/json",
        "Authorization": f"Basic {TALK_BASE64}",
    }
    url = f"{talk_url}/ocs/v2.php/apps/spreed/api/v4/room"
    response = requests.request("POST", url, headers=headers, data=payload, files=[])

    if response.ok:
        result = response.json()
        data = result["ocs"]["data"]
        token = f'{data["token"]}'
        print(f"[Room] [talk] [{datetime.now()}] create {name} ({token}) ok")
        return token
    else:
        print(f"[Room] [talk] [{datetime.now()}] create {name} error")
        return None


def add_user_room(token, username):
    # initialisation
    talk_url = environ["TALK_URL"]
    user = environ["TALK_USER"]
    password = environ["TALK_PASSWORD"]
    payload = {"newParticipant": f"{username}"}
    TALK_BASE64 = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")
    headers = {
        "OCS-APIRequest": "true",
        "Accept": "application/json",
        "Authorization": f"Basic {TALK_BASE64}",
    }

    url = f"{talk_url}/ocs/v2.php/apps/spreed/api/v4/room/{token}/participants"
    response = requests.request("POST", url, headers=headers, data=payload, files=[])

    if response.ok:
        print(f"[Room] [talk] [{datetime.now()}] add {username} room({token}) ok")
    else:
        print(f"[Room] [talk] [{datetime.now()}] add {username} room({token}) error")

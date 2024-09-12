import base64
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

    # print(response.text)

    if response.status_code == 400 or response.ok:
        if response.status_code == 400:
            data = response.json()
            status = data["ocs"]["meta"]["statuscode"]

            if status != 102:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def create_room(name):
    # initialisation
    talk_url = environ["TALK_URL"]
    user = environ["TALK_USER"]
    password = environ["TALK_PASSWORD"]

    TALK_BASE64 = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")

    headers = {
        "Accept": "application/json",
        "OCS-APIRequest": "true",
        "Content-Type": "application/json",
        "Authorization": f"Basic {TALK_BASE64}",
    }

    data = {"roomType": "2", "roomName": name}

    response = requests.post(
        f"{talk_url}/ocs/v2.php/apps/spreed/api/v4/room", headers=headers, data=data
    )

    if response.status_code == 200:
        result = response.json()
        data = result["ocs"]["data"]
        return f'{data["token"]}'
    else:
        return None

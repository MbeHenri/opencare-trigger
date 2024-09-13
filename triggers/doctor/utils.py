import base64
import requests
from datetime import datetime
from triggers.config import environ


# Fonction pour récupérer les docteurs (providers) depuis OpenMRS
def get_doctors():
    # initialisation
    openmrs_url = environ["O3_URL"]
    openmrs_username = environ["O3_USER"]
    openmrs_password = environ["O3_PASSWORD"]

    response = requests.get(
        f"{openmrs_url}/openmrs/ws/rest/v1/provider?v=custom:(uuid,identifier,person:(uuid,display))",
        auth=(openmrs_username, openmrs_password),
    )
    response.raise_for_status()
    return response.json()["results"]


# insertion des doctors dans la base de données du portail des doctors
def insert_doctors_to_talk(doctors):
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

    for doctor in doctors:
        username = doctor["identifier"]

        payload = {
            "userid": username,
            "displayName": doctor["person"]["display"],
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
                    print(
                        f"[Doctor] [doctor] [{datetime.now()}] sync Identifier({username}) error"
                    )
                else:
                    print(
                        f"[Doctor] [doctor] [{datetime.now()}] sync Identifier({username}) exist"
                    )
            else:
                print(
                    f"[Doctor] [doctor] [{datetime.now()}] sync Identifier({username}) created"
                )
        else:
            print(
                f"[Doctor] [doctor] [{datetime.now()}] sync Identifier({username}) error"
            )

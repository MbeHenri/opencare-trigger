from datetime import datetime
import time
import urllib.parse
from triggers.config import get_mongodb_client

from triggers.doctor.utils import get_doctors
from triggers.patient import combinaisons
from triggers.patient.utils import get_patients
from triggers.room.utils import build_room_name


def main():
    print(f"[Room] [{datetime.now()}] init")
    waiting_time = 100

    # loop of the server

    # connection to mongo
    client = get_mongodb_client()
    db = client["opencare"]
    collection = db["rooms"]

    while True:
        print(f"[Room] [{datetime.now()}] start synchronisation")

        # get doctors
        doctors = get_doctors()

        for recherche in combinaisons:
            # Encod search text
            encoded_term = urllib.parse.quote(recherche, safe="")

            # get patients
            patients = get_patients(encoded_term)

            for doctor in doctors:
                for patient in patients:
                    # on verifie s'il n'existe pas de reunion enregistré dans mongo
                    exist = collection.find_one(
                        {
                            "uuidDoctor": doctor["uuid"],
                            "uuidPatient": patient["uuid"],
                        }
                    )
                    # si non on construit le nom Jitsi et on le renseigne dans mongo
                    if exist is None:
                        room_name = build_room_name(
                            doctor["person"]["display"],
                            patient["person"]["display"],
                        )
                        collection.insert_one(
                            {
                                "uuidPatient": patient["uuid"],
                                "uuidDoctor": doctor["uuid"],
                                "roomName": room_name,
                            }
                        )
                        print(
                            f"[Room] [jitsi] [{datetime.now()}] created {room_name}"
                        )
                    else:
                        print(
                            f"[Room] [jitsi] [{datetime.now()}] {exist['roomName']} already exists"
                        )

        print(f"[Room] [{datetime.now()}] end synchronisation")

        # waiting
        time.sleep(waiting_time)

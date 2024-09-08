from datetime import datetime
import time

# import random
from .utils import get_doctors, insert_doctors_to_talk


def main():
    print(f"[Doctor] [{datetime.now()}] init")
    waiting_time = 10

    # loop of the server

    while True:
        print(f"[Doctor] [{datetime.now()}] start synchronisation")

        # get doctors
        doctors = get_doctors()

        # insert and update doctors
        insert_doctors_to_talk(doctors)

        # client.close()
        print(f"[Doctor] [{datetime.now()}] end synchronisation")

        # waiting
        time.sleep(waiting_time)

from datetime import datetime
import time
# import urllib.parse

# import random
from .utils import get_services, insert_services_odoo

from triggers.config import get_odoo_client


def main():
    print(f"[Service] [{datetime.now()}] init")

    # shuffle randomly the combinations
    # random.shuffle(combinaisons)
    # time to sleep
    waiting_time = 10

    # loop of the server

    # connection to odoo
    models, uid = get_odoo_client()

    while True:
        print(f"[Service] [{datetime.now()}] start synchronisation")

        # insert and update Services
        services = get_services()

        # insert Services as customers
        insert_services_odoo(services, models, uid)

        print(f"[Service] [{datetime.now()}] end synchronisation")

        # waiting
        time.sleep(waiting_time)

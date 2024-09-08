from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient
import xmlrpc.client

# chargement des variables d'environnements
load_dotenv()


environ = {
    "O3_URL": getenv("O3_URL"),
    "O3_USER": getenv("O3_USER"),
    "O3_PASSWORD": getenv("O3_PASSWORD"),
    "MONGO_URL": getenv("MONGO_URL"),
    "BASE_PASSWORD_PATIENT": getenv("BASE_PASSWORD_PATIENT", "123456"),
    "ODOO_URL": getenv("ODOO_URL"),
    "ODOO_DB": getenv("ODOO_DB"),
    "ODOO_USER": getenv("ODOO_USER"),
    "ODOO_PASSWORD": getenv("ODOO_API_KEY"),
    "ODOO_CODE_SERVICE": getenv("ODOO_CODE_SERVICE", "OPENCARES"),
    "ODOO_PRICE_SERVICE": getenv("ODOO_PRICE_SERVICE", 1500),
    "TALK_URL": getenv("TALK_URL"),
    "TALK_USER": getenv("TALK_USER"),
    "TALK_PASSWORD": getenv("TALK_PASSWORD"),
    "TALK_INIT_PASSWORD": getenv("TALK_INIT_PASSWORD", "TALK_PASSWORD"),
}

def get_mongodb_client():
    # auth_str = f"{user}:{password}@" if user and password else ""
    # mongo_url = f"mongodb://{auth_str}{host}:{port}/"
    mongo_url = environ["MONGO_URL"]

    # connexion à mongoDB
    client = MongoClient(mongo_url)

    return client


def get_odoo_client():
    # Odoo API endpoint URLs
    ODOO_URL = environ["ODOO_URL"]
    # ODOO_URL = f"http://{host}:{port}"
    ODOO_DB = environ["ODOO_DB"]
    ODOO_USERNAME = environ["ODOO_USER"]
    ODOO_PASSWORD = environ["ODOO_PASSWORD"]

    # Connect to Odoo API
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(ODOO_URL))
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(ODOO_URL))

    return models, uid

import requests
from datetime import datetime
from triggers.config import environ


# Fonction pour récupérer les services depuis OpenMRS
def get_services():
    # initialisation
    openmrs_url = environ["O3_URL"]
    openmrs_username = environ["O3_USER"]
    openmrs_password = environ["O3_PASSWORD"]

    response = requests.get(
        f"{openmrs_url}/openmrs/ws/rest/v1/appointmentService/all/full",
        auth=(openmrs_username, openmrs_password),
    )
    response.raise_for_status()

    return [
        {"name": service["name"], "uuid": service["uuid"]}
        for service in response.json()
    ]


def insert_services_odoo(services, models, uid):
    for service in services:
        product_name = service["name"]
        product_barcode = "{}#{}".format(environ["ODOO_CODE_SERVICE"], service["uuid"])

        product_id = models.execute_kw(
            environ["ODOO_DB"],
            uid,
            environ["ODOO_PASSWORD"],
            "product.template",
            "search",
            [[["barcode", "=", product_barcode]]],
        )

        if product_id:
            print(
                f"[Service] [odoo] [{datetime.now()}] sync Identifier({service['name']}) exist"
            )
        else:
            product_id = models.execute_kw(
                environ["ODOO_DB"],
                uid,
                environ["ODOO_PASSWORD"],
                "product.template",
                "create",
                [
                    {
                        "name": product_name,
                        "barcode": product_barcode,
                        "type": "service",  # 'product', 'consu', 'service'
                        "list_price": float(
                            environ["ODOO_PRICE_SERVICE"]
                        ),  # Selling price
                    }
                ],
            )
            print(
                f"[Service] [odoo] [{datetime.now()}] sync Identifier({service['name']}) created"
            )

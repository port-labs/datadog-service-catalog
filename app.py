## Import the needed libraries
import requests
from decouple import config
from loguru import logger


# Get environment variables using the config object or os.environ["KEY"]
# These are the credentials passed by the variables of your pipeline to your tasks and in to your env

PORT_CLIENT_ID = config("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = config("PORT_CLIENT_SECRET")
DATADOG_API_KEY = config("DATADOG_API_KEY")
DATADOG_APPLICATION_KEY = config("DATADOG_APPLICATION_KEY")
DATADOG_API_URL = config("DATADOG_API_URL")
PORT_API_URL = "https://api.getport.io/v1"


## Get Port Access Token
credentials = {'clientId': PORT_CLIENT_ID, 'clientSecret': PORT_CLIENT_SECRET}
token_response = requests.post(f'{PORT_API_URL}/auth/access_token', json=credentials)
access_token = token_response.json()['accessToken']

# You can now use the value in access_token when making further requests
headers = {
	'Authorization': f'Bearer {access_token}'
}
blueprint_id = 'datadogServiceCatalog'


def add_entity_to_port(entity_object):
    """A function to create the passed entity in Port

    Params
    --------------
    entity_object: dict
        The entity to add in your Port catalog
    
    Returns
    --------------
    response: dict
        The response object after calling the webhook
    """
    response = requests.post(f'{PORT_API_URL}/blueprints/{blueprint_id}/entities?upsert=true&merge=true', json=entity_object, headers=headers)
    logger.info(response.json())


def retrieve_service_catalogs():
    """A function to make API request to Datadog to retrieve Service catalogs"""

    logger.info("fetching service catalog data")
    datadog_headers = {'DD-API-KEY': f'{DATADOG_API_KEY}', 'DD-APPLICATION-KEY': f'{DATADOG_APPLICATION_KEY}', 'Accept': 'application/json'}
    datadog_response = requests.get(f'{DATADOG_API_URL}/api/v2/services/definitions', headers=datadog_headers)
    datadog_response.raise_for_status()
    logger.info("successfully retrieved service catalog data")
    services = datadog_response.json().get("data", [])

    for service in services:
        schema_data = service["attributes"]["schema"]
        entity = {
            "identifier": schema_data["dd-service"],
            "title": schema_data["dd-service"],
            "properties": {
                "contacts": schema_data.get("contacts", []),
                "languages": schema_data.get("languages", []),
                "description": schema_data.get("description"),
                "tags": schema_data.get("tags", []),
                "type": schema_data.get("type")
            },
            "relations": {}
            }
        add_entity_to_port(entity)

if __name__ == "__main__":
    retrieve_service_catalogs()
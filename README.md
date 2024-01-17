# Ingesting Datadog Service Catalog


## Getting started

In this example you will create a`datadogServiceCatalog` blueprint that ingests all service catalogs from your Datadog account. You will then add some python script to make API calls to Datadog REST API and fetch data for your account.

## Service Catalog Blueprint
Create the Monitor blueprint in Port using this schema:

```json 
{
  "identifier": "datadogServiceCatalog",
  "description": "This blueprint represents a Datadog service catalog",
  "title": "Datadog Service Catalog",
  "icon": "Datadog",
  "schema": {
    "properties": {
      "contacts": {
        "type": "array",
        "title": "Contacts"
      },
      "description": {
        "title": "Description",
        "type": "string"
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "title": "Tags"
      },
      "languages": {
        "items": {
          "type": "string"
        },
        "title": "Languages",
        "type": "array"
      },
      "type": {
        "title": "Type",
        "type": "string",
        "enum": [
          "web",
          "db",
          "custom",
          "cache",
          "function",
          "browser",
          "mobile"
        ],
        "enumColors": {
          "web": "lightGray",
          "db": "lightGray",
          "custom": "lightGray",
          "cache": "lightGray",
          "function": "lightGray",
          "browser": "lightGray",
          "mobile": "lightGray"
        }
      },
      "code_repositories": {
        "title": "Code Repositories",
        "type": "array",
        "items": {
          "type": "string",
          "format": "url"
        }
      }
    },
    "required": []
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

## Running the python script

To ingest data from your Datadog account to Port, run the following commands: 

```bash
export PORT_CLIENT_ID=<ENTER CLIENT ID>
export PORT_CLIENT_SECRET=<ENTER CLIENT SECRET>
export DATADOG_API_KEY=<ENTER DATADOG API KEY>
export DATADOG_APPLICATION_KEY=<ENTER DATADOG APPLICATION KEY>
export DATADOG_API_URL=<ENTER DATADOG API URL>

git clone https://github.com/port-labs/datadog-service-catalog.git

cd datadog-service-catalog

pip install -r ./requirements.txt

python app.py
```

The list of variables required to run this script are:
- `PORT_CLIENT_ID`
- `PORT_CLIENT_SECRET`
- `DATADOG_API_KEY`
- `DATADOG_APPLICATION_KEY`
- `DATADOG_API_URL`

Please note that by deafult, all Datadog API clients are configured to consume Datadog US site APIs (https://api.datadoghq.com). If you are on the Datadog EU site, set the environment variable `DATADOG_API_URL` to `https://api.datadoghq.eu`. Some Datadog clients may require you to add your account region to the API. In this case, you may change the DATADOG_API_URL to `https://api.<region>.datadoghq.com` or `https://api.<region>.datadoghq.eu`

Follow the official documentation on how to [generate Datadog API and application keys](https://docs.datadoghq.com/api/latest/)
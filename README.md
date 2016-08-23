# YAPDNS Application

Django application to collect Passive DNS data from YAPDNS clients; display, correlate and analyze them

## Setup

This project uses docker and docker-compose for managing environment and dependencies. There are 4 containers required for the project - elasticsearch, postgres, python/django and nginx.

To start the services

    docker-compose up

To setup django models

    docker-compose run web python manage.py migrate

To setup django admin

    docker-compose run web python manage.py createsuperuser

To setup elasticsearch mappings for DnsRecord document type
    
    docker-compose run web python manage.py index_create --override

## Adding a YAPDNS Client

Login to Django Admin > Client, add client name and copy the `client_id` and `client_secret`. Use these keys in `yapdnsbeat.yml` config file for client.

```yaml
    output.http:
    client_id: 'client id'
    client_secret_key: 'client secret'
    api_endpoint: http://localhost:5050/
    bulk_api_endpoint: http://localhost:5050/bulk
```

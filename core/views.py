from django.http import JsonResponse
from .search import DnsRecord
from .models import Client
from functools import wraps
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
import json

response_map = {
    200: 'DNS Record create successfully',
    400: 'Failed to create DNS Record',
    500: 'Invalid request'
}


def check_client_credentials(client_id, client_secret):
    try:
        Client.objects.filter(id=client_id, secret_key=client_secret)
    except:
        return False
    return True


def client_auth(func):

    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                client_id, client_secret = auth.split(':', 1)
                if check_client_credentials(client_id, client_secret):
                    return func(request, *args, **kwargs)
        return response_from_code(500)
    return _decorator


def response_from_code(code):
    response = {
        'status': code,
        'message': response_map[code]
    }

    return JsonResponse(response, status=code)


def build_record_from_dict(body):
    if all(k not in body for k in ('domain', 'rtype', 'client', 'rdata', 'timestamp')):
        raise Exception

    if body['rtype'] not in ['A', 'AAAA', 'SOA', 'NS', 'PTR', 'CNAME', 'MX', 'SRV']:
        raise Exception

    if 'ttl' in body and int(body['ttl']) < 0:
        raise Exception

    client = body['client']

    if all(k not in client for k in ('service_type', 'ip')):
        raise Exception

    dns_record = DnsRecord(**body)
    return dns_record


@client_auth
def create_record(request):
    if request.method != 'POST':
        return response_from_code(400)

    body = json.loads(request.body)

    try:
        dns_record = build_record_from_dict(body)
        dns_record.save()
    except Exception, e:
        return response_from_code(400)

    return response_from_code(200)


@client_auth
def create_record_bulk(request):
    if request.method != 'POST':
        return response_from_code(400)

    dns_records = []
    body = json.loads(request.body)
    for record in body:
        try:
            dns_record = build_record_from_dict(record)
        except Exception:
            return response_from_code(400)
        dns_records.append(dns_record)

    bulk(connections.get_connection(), (d.to_dict(True) for d in dns_records))

    return response_from_code(200)

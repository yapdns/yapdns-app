from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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


class InvalidDnsRecord(Exception):
    pass


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


def response_from_code(code, message=None):
    message = message if message else response_map[code]
    response = {
        'status': code,
        'message': message
    }

    return JsonResponse(response, status=code)


def build_record_from_dict(body):
    required_fields = ('domain', 'rtype', 'client', 'rdata', 'timestamp')
    if not all(k in body for k in required_fields):
        raise InvalidDnsRecord('Required fields {} not present'.format(required_fields))

    if body['rtype'] not in ['A', 'AAAA', 'SOA', 'NS', 'PTR', 'CNAME', 'MX', 'SRV']:
        raise InvalidDnsRecord('Invalid value for record type')

    if 'ttl' in body and int(body['ttl']) < 0:
        raise InvalidDnsRecord('Invalid value for TTL')

    client = body['client']
    client_fields = ('service_type', 'ip')
    if not all(k in client for k in client_fields):
        raise InvalidDnsRecord('Required fields {} not present in client'.format(client_fields))

    dns_record = DnsRecord(**body)
    return dns_record


@csrf_exempt
@client_auth
def create_record(request):
    if request.method != 'POST':
        return response_from_code(400)

    body = json.loads(request.body)

    try:
        dns_record = build_record_from_dict(body)
        dns_record.save()
    except Exception, e:
        return response_from_code(400, str(e))

    return response_from_code(200)

@csrf_exempt
@client_auth
def create_record_bulk(request):
    if request.method != 'POST':
        return response_from_code(400)

    dns_records = []
    body = json.loads(request.body)
    for record in body:
        try:
            dns_record = build_record_from_dict(record)
        except Exception, e:
            return response_from_code(400, str(e))
        dns_records.append(dns_record)

    bulk(connections.get_connection(), (d.to_dict(True) for d in dns_records))

    return response_from_code(200)


def search_records(request):
    domain = request.GET['domain']
    s = DnsRecord.search()
    s = s.filter('term', domain=domain)
    results = s.execute()

    response = []

    for record in results:
        response.append({
            'timestamp': record['timestamp'],
            'domain': record['domain'],
            'type': record['rtype'],
            'data': record['rdata'],
            # 'client': dict(record['client'])
            })

    return JsonResponse(response, safe=False)


def home(request):
    return render(request, 'core/index.html')

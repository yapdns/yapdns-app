from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .search import DnsRecord
import json

response_map = {
    200: 'DNS Record create successfully',
    500: 'Failed to create DNS Record',
    400: 'Invalid request'
}


def response_from_code(code):
    response = {
        'status': code,
        'message': response_map[code]
    }

    return JsonResponse(response, status=code)


@csrf_exempt
def create_record(request):
    if request.method != 'POST':
        return response_from_code(200)

    body = json.loads(request.body)
    domain = body['domain']
    rtype = body['rtype']
    rdata = body['rdata']
    ttl = body['ttl']

    client = body['client']

    dns_record = DnsRecord(domain=domain, rtype=rtype, rdata=rdata, ttl=ttl, client=client)
    dns_record.save()
    return response_from_code(200)

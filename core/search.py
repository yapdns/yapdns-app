from django.conf import settings

from elasticsearch_dsl import DocType, Date, String, Long, Ip, Nested, \
    Object, Index, MetaField, analyzer, FacetedSearch, Q, TermsFacet, \
    InnerObjectWrapper, DateHistogramFacet, SF


class Client(InnerObjectWrapper):
    pass


class DnsRecord(DocType):
    domain = String(index='not_analyzed')
    rtype = String(index='not_analyzed')
    rdata = String(index='not_analyzed')
    ttl = Long(index='not_analyzed')
    client = Nested(
        doc_class=Client,
        properties={
            'service_type': String(index='not_analyzed'),
            'ip': Ip(index='not_analyzed')
        }
    )
    created_at = Date()

# create an index and register the doc types
index = Index(settings.ES_INDEX)
index.settings(**settings.ES_INDEX_SETTINGS)
index.doc_type(DnsRecord)

from django.conf import settings

from elasticsearch_dsl import DocType, Date, String, Long, Ip, Nested, \
    Object, Index, MetaField, analyzer, FacetedSearch, Q, TermsFacet, \
    InnerObjectWrapper, DateHistogramFacet, SF


class Client(InnerObjectWrapper):
    pass


class DnsRecord(DocType):
    domain = String()
    rtype = String()
    rdata = String()
    ttl = Long()
    client = Nested(
        doc_class=Client,
        properties={
            'service_type': String(),
            'ip': Ip()
        }
    )
    created_at = Date()

# create an index and register the doc types
index = Index(settings.ES_INDEX)
index.settings(**settings.ES_INDEX_SETTINGS)
index.doc_type(DnsRecord)

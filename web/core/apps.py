from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

from elasticsearch_dsl.connections import connections
from elasticsearch.exceptions import NotFoundError


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = "Core"

    def ready(self):
        connections.configure(**settings.ES_CONNECTIONS)

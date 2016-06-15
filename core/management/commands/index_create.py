from django.core.management.base import BaseCommand, CommandError
from elasticsearch_dsl.connections import connections

from core.search import index


class Command(BaseCommand):
    help = 'Create elasticsearch indexes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--override',
            action='store_true',
            dest='override',
            default=False,
            help='Override mappings - this will delete existing data',
        )

    def handle(self, *args, **options):
        """
            check if index exists
                is the mapping same?
                    override

        """
        self.es = connections.get_connection()
        if options['override']:
            index.delete(ignore=404)
        index.create()

from django.core.management.base import BaseCommand
from services.generate_json_fixtures import create_fixtures


class Command(BaseCommand):
    help = 'Creating fixtures for database'

    def handle(self, **options):
        create_fixtures()
        self.stdout.write('Fixtures was successful created')

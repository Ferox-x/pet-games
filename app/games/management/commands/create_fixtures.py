from django.core.management.base import BaseCommand
from services.generate_json_fixtures import create_fixtures


class Command(BaseCommand):
    """Basecommand для генерации фикстур для таблиц schulte, stroop, users."""

    help = 'Creating fixtures for database'

    def handle(self, **options) -> None:
        create_fixtures()
        self.stdout.write('Fixtures was successful created')

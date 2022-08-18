from django.core.management import call_command
from django.test import TestCase


class LeaderboardsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('makefixtures')
        call_command('loaddata', '/*.json')


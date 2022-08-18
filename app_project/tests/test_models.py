from django.utils.translation import activate
from django.contrib.auth import get_user_model
from django.test import TestCase

from games.models import SchulteModel, StroopModel
from support.models import SupportTicket, Chat

User = get_user_model()
activate('en-en')


class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание обьектов в моделях."""

        super().setUpClass()
        cls.user = User.objects.create(
            username='TestUser',
            is_superuser=True,
            id='1'
        )

        cls.ticket = SupportTicket.objects.create(
            header='TestHeader',
            first_message='message',
            user_id='1',
            id='1'
        )

        cls.chat = Chat.objects.create(
            ticket_id='1',
            user_id='1',
            message='message',
        )

        cls.schulte = SchulteModel.objects.create(
            id='1',
            user_id='1',
            record='1661'
        )

        cls.stroop = StroopModel.objects.create(
            id='1',
            user_id='1',
            record='1 - 1 - 1',
            score='1500'
        )

    def test_models_have_correct_object_names(self):
        user = ModelTest.user
        expected_object_name = user.username
        self.assertEqual(expected_object_name, str(user))

        ticket = ModelTest.ticket
        expected_object_name = ticket.header
        self.assertEqual(expected_object_name, str(ticket))

    def test_user_verbose_name(self):
        user = User
        field_verboses = {
            'username': 'Username',
            'country': 'Country',
            'description': 'Description',
            'email': 'Email address',
            'full_name': 'Full name',
            'image': 'image',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(user._meta.get_field(value).verbose_name,
                                 expected)

    def test_ticket_verbose_name(self):
        user = SupportTicket
        field_verboses = {
            'first_message': 'First message',
            'status': 'Status',
            'date': 'Date',
            'header': 'Header',
            'user': 'User',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(user._meta.get_field(value).verbose_name,
                                 expected)

    def test_chat_verbose_name(self):
        user = Chat
        field_verboses = {
            'ticket': 'Ticket',
            'message': 'Message',
            'date': 'Date',
            'user': 'User',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(user._meta.get_field(value).verbose_name,
                                 expected)

    def test_schulte_verbose_name(self):
        user = SchulteModel
        field_verboses = {
            'record': 'Record Time',
            'date': 'Time',
            'user': 'User',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(user._meta.get_field(value).verbose_name,
                                 expected)

    def test_stroop_verbose_name(self):
        user = StroopModel
        field_verboses = {
            'record': 'Record',
            'date': 'Time',
            'user': 'User',
            'score': 'Score'
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(user._meta.get_field(value).verbose_name,
                                 expected)

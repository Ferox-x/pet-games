from django.test import TestCase
from django.utils import timezone
from django.utils.formats import localize

from services.support_services import Support, SupportStaff
from support.models import SupportTicket, Chat
from users.models import Users


class SupportTest(TestCase):
    date = timezone.now()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создание экземпляров."""
        user = Users.objects.create(
            username='TestUser',
            country='RU',
            email='admin@mail.com',
            is_support=True,
            is_active=True,
            is_superuser=True,
        )
        ticket = SupportTicket.objects.create(
            user=user, header='TestHeader', status='OP',
            first_message='Test First Message', date=cls.date,
        )
        Chat.objects.create(
            ticket=ticket, message='Test Chat Message', user=user,
            date=cls.date
        )

    def setUp(self) -> None:
        self.user = Users.objects.get(username='TestUser')
        self.ticket = SupportTicket.objects.get(header='TestHeader')

    def test_support_manager_get_chat_from_ticket(self):
        """Тест на получение чата по тикету."""

        post_data = {
            'get_chat_from_ticket': 'True',
            'ticket_id': self.ticket.id
        }
        message = Support(self.user, post_data).manager()
        message_equal = {
            0: {
                'message': 'Test Chat Message',
                'date': localize(self.date),
                'user__username': 'TestUser',
                'id': 1, 'user__image': ''
            },
            'len': 1,
            'ticket': {
                'header': 'TestHeader',
                'date': localize(self.date),
                'first_message': 'Test First Message', 'status': 'OP'
            }
        }
        self.assertEqual(message, message_equal, '')

    def test_support_manager_create_ticket(self):
        """Тест на создание тикета."""
        post_data = {
            'create_ticket': 'True',
            'header': 'Create Ticket Test',
            'chat_message': 'Create Ticket Test Message',
        }
        Support(self.user, post_data).manager()
        first_message = SupportTicket.objects.get(id=2).first_message
        self.assertEqual(first_message, post_data.get('chat_message'))

    def test_support_manager_add_message_to_chat(self):
        """Тест на добавление сообщение к чату."""
        post_data = {
            'add_message_to_chat': 'True',
            'chat_message': 'Test Message',
            'ticket_id': 1,
        }
        message = Support(self.user, post_data).manager().get('message')
        self.assertEqual(message, post_data.get('chat_message'))

    def test_support_staff_manager_change_status(self):
        """Тест на смену статуса тикета"""
        post_data = {
            'change_status': 'True',
            'status': 'IP',
            'ticket_id': 1,
        }
        SupportStaff(self.user, post_data).manager()
        ticket = SupportTicket.objects.get(status='IP')
        self.assertEqual(ticket.status, 'IP')

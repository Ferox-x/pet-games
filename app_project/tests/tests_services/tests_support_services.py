from django.test import TestCase
from django.utils import timezone
from django.utils.formats import localize

from services.support_services import Support, SupportStaff
from support.models import SupportTicket, Chat
from users.models import Users


class SupportTest(TestCase):
    """Класс тестов службы поддержки."""
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

    def test_support_manager_create_ticket(self):
        """Тест на создание тикета."""
        post_data = {
            'create_ticket': 'True',
            'header': 'Create Ticket Test',
            'chat_message': 'Create Ticket Test Message',
        }
        Support(self.user, post_data).manager()
        first_message = SupportTicket.objects.get(first_message='Create Ticket Test Message').first_message
        self.assertEqual(first_message, post_data.get('chat_message'))

    def test_support_get_sorted_tickets(self):
        op_ticket = SupportTicket.objects.create(
            user=self.user, header='Test Open', status='OP',
            first_message='Test OpenTest Open')
        ip_ticket = SupportTicket.objects.create(
            user=self.user, header='Test In Progress', status='IP',
            first_message='Test In Progress Test In Progress')
        cl_ticket = SupportTicket.objects.create(
            user=self.user, header='Test Closed', status='CL',
            first_message='Test ClosedTest Closed')

        tickets = SupportTicket.objects.select_related(
            'user'
        ).values(
            'header', 'date', 'status', 'first_message', 'id'
        ).all()

        sorted_tickets = Support._get_sorted_tickets(tickets)

        self.assertEqual(sorted_tickets.get('op')[0].get('status'), 'OP')
        self.assertEqual(sorted_tickets.get('ip')[0].get('status'), 'IP')
        self.assertEqual(sorted_tickets.get('cl')[0].get('status'), 'CL')

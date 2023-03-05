from django.contrib.auth import get_user_model, get_user
from django.test import Client, TestCase
from http import HTTPStatus

from django.core.management import call_command

User = get_user_model()


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Загрузка фикстур в тестовую БД и создание пользователя."""

        super().setUpClass()
        call_command('makefixtures')
        call_command('loaddata', 'fixtures/user.json')
        call_command('loaddata', 'fixtures/stroop_leaderboard.json')
        call_command('loaddata', 'fixtures/schulte_leaderboard.json')

        cls.user = User.objects.create(
            username='TestUser',
            is_superuser=True
        )

    def setUp(self) -> None:
        """Авторизация пользователя."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_loging(self) -> None:
        """Проверка аунтефикации пользователя."""
        self.assertTrue(
            get_user(self.authorized_client).is_authenticated,
            'Пользователь не прошёл аутентификацию.'
        )

    def test_urls_exists_at_desired_location_avilable_to_any(self):
        """Проверка доступности ulr для всех пользователей."""
        url_names_http_status = {
            '/': HTTPStatus.OK,
            '/about/': HTTPStatus.OK,
            '/api/v1/schulte/': HTTPStatus.OK,
            '/api/v1/stroop/': HTTPStatus.OK,
            '/games/schulte/': HTTPStatus.OK,
            '/games/stroop/': HTTPStatus.OK,
            '/games/leaderboards/schulte/': HTTPStatus.OK,
            '/games/leaderboards/stroop/': HTTPStatus.OK,
            '/users/TestUser/': HTTPStatus.OK,
            '/support/': HTTPStatus.FOUND,
            '/users/profile/': HTTPStatus.FOUND,

        }
        for url, http_status in url_names_http_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    http_status,
                    f'Гость не получил статус 200 (ОК).'
                    f' Получен код: {response.status_code}'
                )

    def test_urls_exists_at_desired_location_avilable_to_authorized(self):
        """Проверка доступности ulr для авторизированных пользователей."""
        url_names_http_status = {
            '/support/': HTTPStatus.OK,
            '/users/profile/': HTTPStatus.OK,
        }
        for url, http_status in url_names_http_status.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.status_code,
                    http_status,
                    f'Авторизированный пользователь не получил статус 200 (ОК).'
                    f'Получен код: {response.status_code}'
                )

    def test_urls_uses_correct_template(self):
        """Проверка соотвествия шаблона для заданного ulr."""
        url_names_templates = {
            '/': 'core/main_page/main_page.html',
            '/about/': 'about/about.html',
            '/games/schulte/': 'games/schulte/index.html',
            '/games/stroop/': 'games/stroop/index.html',
            '/games/leaderboards/schulte/': 'games/leaderboards/leaderboards.html',
            '/games/leaderboards/stroop/': 'games/leaderboards/leaderboards.html',
            '/users/TestUser/': 'users/profile_detail.html',
            '/users/profile/': 'users/profile.html',
            '/support/': 'support/support.html',
            '/support/staff/': 'support/support.html'

        }
        for url, template in url_names_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Шаблон не соотвествует ожидаемому.'
                )

    def test_urls_correct_redirect_to_guest_clients(self):
        url_names_http_status = {
            '/support/': HTTPStatus.FOUND,
            '/users/profile/': HTTPStatus.FOUND,
        }
        for url, http_status, in url_names_http_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, http_status)

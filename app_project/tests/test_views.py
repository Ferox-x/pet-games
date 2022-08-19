import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django import forms

from games.models import SchulteModel, StroopModel
from support.models import SupportTicket, Chat
from users.models import Users

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ViewsTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpClass(cls):
        """Создание обьектов в моделях."""
        super().setUpClass()
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B')

        uploaded = SimpleUploadedFile(name='small.gif',
                                      content=small_gif,
                                      content_type='image/gif')

        cls.user = User.objects.create(
            username='TestUser',
            description='description',
            email='email@email.ru',
            full_name='Full Name',
            country='RU',
            is_superuser=True,
            id='1',
            image=uploaded
        )

    def setUp(self) -> None:
        """Авторизация пользователя."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка использования корректных шаблонов."""
        templates_page_names = {
            reverse('core:main'): 'core/main_page/main_page.html',
            reverse('about:about'): 'about/about.html',
            reverse('game:schulte'): 'games/schulte/index.html',
            reverse('game:stroop'): 'games/stroop/index.html',
            reverse('users:profile_detail', kwargs={'slug': 'TestUser'}):
                'users/profile_detail.html',
            reverse('users:profile'): 'users/profile.html',
            reverse('support:support'): 'support/support.html',
            reverse('support:support_staff'): 'support/support_staff.html'
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name,
                                                      follow=True)
                self.assertTemplateUsed(response, template)

    def test_profile_page_show_correct_form_fields(self):
        response = self.authorized_client.get(reverse('users:profile'))
        form_fields = {
            'username': forms.fields.CharField,
            'description': forms.fields.CharField,
            'full_name': forms.fields.CharField,
            'email': forms.fields.CharField,
            'country': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_profile_page_show_correct_image_fields(self):
        response = self.authorized_client.get(reverse('users:profile'))
        form_fields = {
            'image': forms.fields.FileField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('image').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('users:profile'))
        get_context: Users = response.context.get('user')

        username = get_context.username
        full_name = get_context.full_name
        email = get_context.email
        country = get_context.country

        self.assertEqual(username, self.user.username)
        self.assertEqual(full_name, self.user.full_name)
        self.assertEqual(email, self.user.email)
        self.assertEqual(country, self.user.country)

    def test_image_exists_at_profile_page(self):
        response = self.authorized_client.get(reverse('users:profile'))
        page = response.context.get('user').image
        self.assertTrue(page == 'user_images/small.gif')

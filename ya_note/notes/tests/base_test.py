from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()

SLUG = 'post_t'
URL_HOME = reverse('notes:home')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_NOTES_LIST = reverse('notes:list')
URL_NOTES_ADD = reverse('notes:add')
URL_NOTES_SUCCESS = reverse('notes:success')
URL_NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
URL_NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_NOTES_DELETE = reverse('notes:delete', args=(SLUG,))
REDIRECT_URL_NOTES_ADD = f'{URL_LOGIN}?next={URL_NOTES_ADD}'
REDIRECT_URL_NOTES_LIST = f'{URL_LOGIN}?next={URL_NOTES_LIST}'
REDIRECT_URL_NOTES_SUCCESS = f'{URL_LOGIN}?next={URL_NOTES_SUCCESS}'
REDIRECT_URL_NOTES_DETAIL = f'{URL_LOGIN}?next={URL_NOTES_DETAIL}'
REDIRECT_URL_NOTES_EDIT = f'{URL_LOGIN}?next={URL_NOTES_EDIT}'
REDIRECT_URL_NOTES_DELETE = f'{URL_LOGIN}?next={URL_NOTES_DELETE}'
EXPECTED_URL = f'{URL_LOGIN}?next={URL_NOTES_ADD}'


class TestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Миша')
        cls.reader = User.objects.create(username='Яша')
        cls.client_author = Client()
        cls.client_author.force_login(cls.author)
        cls.client_reader = Client()
        cls.client_reader.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Тест заголовок',
            text='Тест текст',
            slug=SLUG,
            author=cls.author,
        )
        cls.form_data = {'title': 'NEW_TITLE',
                         'text': 'NEW_TEXT',
                         'slug': 'NEW_SLUG'
                         }

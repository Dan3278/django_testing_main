from datetime import datetime, timedelta
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
import pytest
from news.models import News, Comment
TOTAL_COMMENT = 10

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')

@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client

@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )
    return comment

@pytest.fixture
def lot_news():
    News.objects.bulk_create(
        News(
            title="Новость",
            text='Текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE
                           )
    )


@pytest.fixture
def lot_comments(author, news):
    today = timezone.now()
    for index in range(TOTAL_COMMENT):
        comment = Comment.objects.create(
            text=f"Текст{index}",
            news=news,
            author=author,
        )
        comment.created = today + timedelta(days=index)
        comment.save()


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def detail_news_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(
    db
):
    pass

@pytest.fixture
def url_news_detail(news):
    return reverse('news:detail', args=(news.id,))

@pytest.fixture
def url_edit_comment(comment):
    return reverse('news:edit', args=(comment.id,))

@pytest.fixture
def url_delete_comment(comment):
    return reverse('news:delete', args=(comment.id,))

@pytest.fixture
def url_home():
    return reverse('news:home')

@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def redirect_url_delete_comment(url_login,
                                url_delete_comment):
    return f"{url_login}?next={url_delete_comment}"


@pytest.fixture
def redirect_url_edit_comment(url_login, url_edit_comment):
    return f"{url_login}?next={url_edit_comment}"


@pytest.fixture
def redirect_url_detail_news(detail_news_url):
    return f"{detail_news_url}/comments"

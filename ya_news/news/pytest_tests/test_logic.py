from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {
    'text': 'Новый текст',
}
EVIL_WORDS = [
    {'text': f'Комментарий, {word}, комментарий'} for word in BAD_WORDS
]

def assert_comment_count(expected_count):
    """Вспомогательная функция для проверки количества комментариев."""
    assert Comment.objects.count() == expected_count

def assert_comment_fields(comment, expected_data):
    """Проверяет, что поля комментария соответствуют ожидаемым значениям."""
    assert comment.text == expected_data['text']
    assert comment.author == expected_data['author']
    assert comment.news == expected_data['news']

def test_anon_cannot_add_comments(client, detail_news_url):
    client.post(detail_news_url, data=FORM_DATA)
    assert_comment_count(0)

def test_author_can_delete_comment(author_client, delete_comment_url, redirect_url_to_detail, comment):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, redirect_url_to_detail)
    assert_comment_count(0)

def test_user_cant_delete_comment_of_other_users(not_author_client, delete_comment_url, comment):
    """Нельзя удалять чужие комментарии."""
    initial_comment_count = Comment.objects.count()
    response = not_author_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert_comment_count(initial_comment_count)

def test_author_can_edit_comment(author_client, comment, edit_comment_url, redirect_url_to_detail):
    """Автор может изменять свои комментарии."""
    response = author_client.post(edit_comment_url, data=FORM_DATA)
    assertRedirects(response, redirect_url_to_detail)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert_comment_fields(updated_comment, {**FORM_DATA, 'author': comment.author, 'news': comment.news})

@pytest.mark.django_db
def test_user_cant_delete_comment_of_other_users(author_client, delete_comment_url, comment):
    """Нельзя удалять чужие комментарии."""
    response = author_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.FOUND
    assert_comment_count(0)

@pytest.mark.parametrize('evil_words', EVIL_WORDS)
def test_posting_evil_comment(author_client, detail_news_url, evil_words):
    response = author_client.post(detail_news_url, data=evil_words)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert 'text' in response.context['form'].errors
    assert any(WARNING in msg for msg in response.context['form'].errors['text'])
    assert_comment_count(0)

def test_authorized_user_can_create_comment(author_client, author, detail_news_url, news, redirect_url_to_detail):
    Comment.objects.all().delete()
    response = author_client.post(detail_news_url, data=FORM_DATA)
    assertRedirects(response, redirect_url_to_detail)
    assert_comment_count(1)
    comment = Comment.objects.get()
    assert_comment_fields(comment, {**FORM_DATA, 'author': author, 'news': news})

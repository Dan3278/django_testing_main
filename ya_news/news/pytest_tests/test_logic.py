from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


FORM_DATA = {
    'text': 'Новый текст',
}
EVIL_WORDS = [
    {'text': f'Комментарий, {word}, комментарий'} for word
    in BAD_WORDS
]


def test_anon_cannot_add_comments(
    client,
    detail_news_url,
):
    client.post(detail_news_url, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client,
    delete_comment_url,
    detail_news_url,
    redirect_url_to_detail
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, redirect_url_to_detail)
    assert Comment.objects.count() == 0


def test_not_author_cannot_edit_comment(
    not_author_client, comment, edit_comment_url
):
    """Не автор НЕ может изменять чужие коментарии."""
    response = not_author_client.post(edit_comment_url,
                                      data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == comment.text
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_author_can_edit_comment(
    author_client, comment, edit_comment_url,
    detail_news_url, redirect_url_to_detail
):
    """Автор может изменять свои комментарии."""
    response = author_client.post(edit_comment_url,
                                  data=FORM_DATA)
    assertRedirects(response, redirect_url_to_detail)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


@pytest.mark.django_db
def test_user_cant_delete_comment_of_other_users(author_client,
                                                 delete_comment_url):
    """Нельзя удалять чужие коментарии."""
    response = author_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.parametrize('evil_words', EVIL_WORDS)
def test_posting_evil_comment(author_client,
                              detail_news_url, evil_words):
    response = author_client.post(detail_news_url,
                                  data=evil_words)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert 'text' in response.context['form'].errors
    assert any(
        WARNING in msg for msg in
        response.context['form'].errors['text']
    )
    assert Comment.objects.count() == 0


def test_authorized_user_can_create_comment(
    author_client, author, detail_news_url, news,
    redirect_url_to_detail
):
    Comment.objects.all().delete()
    response = author_client.post(detail_news_url,
                                  data=FORM_DATA)
    assertRedirects(response, redirect_url_to_detail)
    assert Comment.objects.all().count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news

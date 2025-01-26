from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


TEST_COMMENT = {'text': 'test комментарий'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data=TEST_COMMENT)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authorized_user_can_create_comment(auth_client,
                                            news,
                                            detail_url,
                                            author):
    response = auth_client.post(detail_url, data=TEST_COMMENT)
    assertRedirects(
        response,
        f'{detail_url}#comments',
        status_code=HTTPStatus.FOUND
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == TEST_COMMENT['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(auth_client, bad_word, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, Какой-то текст'}
    response = auth_client.post(detail_url, data=bad_words_data)
    assert response.status_code == HTTPStatus.OK
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_delete_comment(auth_client, delete_url, detail_url):
    response = auth_client.delete(delete_url)
    assertRedirects(response, f'{detail_url}#comments',
                    status_code=HTTPStatus.FOUND)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(edit_url, create_comment,
                                 auth_client, detail_url):
    response = auth_client.post(edit_url, data=TEST_COMMENT)
    assertRedirects(response, f'{detail_url}#comments',
                    status_code=HTTPStatus.FOUND)
    updated_comment = Comment.objects.get(id=create_comment.id)
    assert updated_comment.text == TEST_COMMENT['text']
    assert updated_comment.news == create_comment.news
    assert updated_comment.author == create_comment.author


@pytest.mark.django_db
def test_user_cant_delete_comment_of_other_users(auth_client, delete_url):
    response = auth_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_edit_comment_of_other_users(
        create_comment,
        auth_reader,
        edit_url,
        reader):
    response = auth_reader.post(edit_url, data=TEST_COMMENT)
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged_comment = Comment.objects.get(id=create_comment.id)
    assert unchanged_comment.text == create_comment.text
    assert unchanged_comment.news == create_comment.news
    assert unchanged_comment.author == create_comment.author

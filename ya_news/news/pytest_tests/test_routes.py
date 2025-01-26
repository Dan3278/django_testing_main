from http import HTTPStatus

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('url_fixture', [
    pytest.lazy_fixture('url_home'),
    pytest.lazy_fixture('detail_news_url'),
    pytest.lazy_fixture('url_login'),
    pytest.lazy_fixture('url_logout'),
    pytest.lazy_fixture('url_signup')
]
)
def test_pages_availability(client, url_fixture):
    response = client.get(url_fixture)
    assert response.status_code == HTTPStatus.OK


@ pytest.mark.django_db
@ pytest.mark.parametrize('client_fixture, expected_status', [
    (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    (pytest.lazy_fixture('client'), HTTPStatus.FOUND)
]
)
@ pytest.mark.parametrize('url_fixture', [
    pytest.lazy_fixture('edit_comment_url'),
    pytest.lazy_fixture('delete_comment_url')
]
)
def test_availability_for_comment_edit_and_delete(client_fixture,
                                                  expected_status,
                                                  url_fixture
                                                  ):
    response = client_fixture.get(url_fixture)
    assert response.status_code == expected_status


@ pytest.mark.django_db
@ pytest.mark.parametrize('url_fixture', [
    pytest.lazy_fixture('edit_comment_url'),
    pytest.lazy_fixture('delete_comment_url')
]
)
def test_redirect_for_anonymous_client(client, url_fixture, url_login):
    redirect_url = f'{url_login}?next={url_fixture}'
    response = client.get(url_fixture)
    assert response.url == redirect_url

from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('url_fixture', [
    pytest.lazy_fixture('home_url'),
    pytest.lazy_fixture('detail_url'),
    pytest.lazy_fixture('login_url'),
    pytest.lazy_fixture('logout_url'),
    pytest.lazy_fixture('signup_url')
]
)
def test_pages_availability(client, url_fixture):
    response = client.get(url_fixture)
    assert response.status_code == HTTPStatus.OK


@ pytest.mark.django_db
@ pytest.mark.parametrize("client_fixture, expected_status", [
    (pytest.lazy_fixture('auth_client'), HTTPStatus.OK),
    (pytest.lazy_fixture('client'), HTTPStatus.FOUND)
]
)
@ pytest.mark.parametrize("url_fixture", [
    pytest.lazy_fixture('edit_url'),
    pytest.lazy_fixture('delete_url')
]
)
def test_availability_for_comment_edit_and_delete(client_fixture,
                                                  expected_status,
                                                  url_fixture
                                                  ):
    response = client_fixture.get(url_fixture)
    assert response.status_code == expected_status


@ pytest.mark.django_db
@ pytest.mark.parametrize("url_fixture", [
    pytest.lazy_fixture('edit_url'),
    pytest.lazy_fixture('delete_url')
]
)
def test_redirect_for_anonymous_client(client, url_fixture):
    login_url = reverse('users:login')
    redirect_url = f'{login_url}?next={url_fixture}'
    response = client.get(url_fixture)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url

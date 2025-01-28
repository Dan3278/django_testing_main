from http import HTTPStatus
import pytest

EXPECTED_OK = HTTPStatus.OK
EXPECTED_NOT_FOUND = HTTPStatus.NOT_FOUND
EXPECTED_REDIRECT = HTTPStatus.FOUND
URL_HOME = pytest.lazy_fixture('url_home')
URL_DETAIL_NEWS = pytest.lazy_fixture('detail_news_url')
URL_LOGIN = pytest.lazy_fixture('url_login')
URL_LOGOUT = pytest.lazy_fixture('url_logout')
URL_SIGNUP = pytest.lazy_fixture('url_signup')
EDIT_COMMENT_URL = pytest.lazy_fixture('edit_comment_url')
DELETE_COMMENT_URL = pytest.lazy_fixture('delete_comment_url')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
REDIRECT_URL = pytest.lazy_fixture('redirect_url')
ANONYMOUS_CLIENT = pytest.lazy_fixture('client')


@pytest.mark.parametrize('url_fixture, client_fixture, expected_status',
                         [
                             (URL_HOME, AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_DETAIL_NEWS, AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_LOGIN, AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_LOGOUT, AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_SIGNUP, AUTHOR_CLIENT, EXPECTED_OK),
                             (EDIT_COMMENT_URL, AUTHOR_CLIENT, EXPECTED_OK),
                             (DELETE_COMMENT_URL, AUTHOR_CLIENT, EXPECTED_OK),
                             (EDIT_COMMENT_URL, NOT_AUTHOR_CLIENT,
                              EXPECTED_NOT_FOUND),
                             (DELETE_COMMENT_URL, NOT_AUTHOR_CLIENT,
                              EXPECTED_NOT_FOUND),
                             (URL_LOGIN, NOT_AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_SIGNUP, NOT_AUTHOR_CLIENT, EXPECTED_OK),
                             (URL_HOME, NOT_AUTHOR_CLIENT, EXPECTED_OK),
                             (EDIT_COMMENT_URL, NOT_AUTHOR_CLIENT,
                              EXPECTED_NOT_FOUND),
                             (DELETE_COMMENT_URL, NOT_AUTHOR_CLIENT,
                              EXPECTED_NOT_FOUND),
                             (EDIT_COMMENT_URL, ANONYMOUS_CLIENT,
                              HTTPStatus.FOUND),
                             (DELETE_COMMENT_URL, ANONYMOUS_CLIENT,
                              HTTPStatus.FOUND)
                         ]
                         )
def test_pages_availability(url_fixture, client_fixture, expected_status):
        """
        Проверяет доступность страницы для заданного URL и ожидаемого статуса.
        """
    response = client_fixture.get(url_fixture)
    assert response.status_code == expected_status


@ pytest.mark.django_db
@ pytest.mark.parametrize('url_fixture', [
    pytest.lazy_fixture('edit_comment_url'),
    pytest.lazy_fixture('delete_comment_url')
]
)
def test_redirect_for_anonymous_client(client,
                                       url_fixture,
                                       url_login,
                                       redirect_url):
    """
    Проверяет редирект для анонимного клиента при доступе к защищенным URL.
    """
    response = client.get(url_fixture)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url(url_fixture)

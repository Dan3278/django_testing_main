from http import HTTPStatus
from .base_test import (
    TestBase,
    REDIRECT_URL_NOTES_ADD, REDIRECT_URL_NOTES_LIST,
    REDIRECT_URL_NOTES_SUCCESS, REDIRECT_URL_NOTES_DETAIL,
    REDIRECT_URL_NOTES_EDIT, REDIRECT_URL_NOTES_DELETE,
    URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP,
    URL_NOTES_LIST,
    URL_NOTES_ADD, URL_NOTES_SUCCESS, URL_NOTES_EDIT,
    URL_NOTES_DETAIL, URL_NOTES_DELETE,
)


class TestRoutes(TestBase):
    def test_http_status_codes(self):
        for url, user, status in (
            (URL_NOTES_ADD, self.client_reader,
             HTTPStatus.OK),
            (URL_NOTES_LIST, self.client_reader,
             HTTPStatus.OK),
            (URL_NOTES_SUCCESS, self.client_reader,
             HTTPStatus.OK),
            (URL_NOTES_DETAIL, self.client_reader,
             HTTPStatus.NOT_FOUND),
            (URL_NOTES_EDIT, self.client_reader,
             HTTPStatus.NOT_FOUND),
            (URL_NOTES_DELETE, self.client_reader,
             HTTPStatus.NOT_FOUND),
            (URL_HOME, self.client_reader,
             HTTPStatus.OK),
            (URL_LOGIN, self.client_reader,
             HTTPStatus.OK),
            (URL_LOGOUT, self.client_reader,
             HTTPStatus.OK),
            (URL_SIGNUP, self.client_reader,
             HTTPStatus.OK),
            (URL_NOTES_ADD, self.client_author,
             HTTPStatus.OK),
            (URL_NOTES_LIST, self.client_author,
             HTTPStatus.OK),
            (URL_NOTES_SUCCESS, self.client_author,
             HTTPStatus.OK),
            (URL_NOTES_DETAIL, self.client_author,
             HTTPStatus.OK),
            (URL_NOTES_EDIT, self.client_author,
             HTTPStatus.OK),
            (URL_NOTES_DELETE, self.client_author,
             HTTPStatus.OK),
            (URL_HOME, self.client_author,
             HTTPStatus.OK),
            (URL_LOGIN, self.client_author,
             HTTPStatus.OK),
            (URL_LOGOUT, self.client_author,
             HTTPStatus.OK),
            (URL_SIGNUP, self.client_author,
             HTTPStatus.OK),
            (URL_HOME, self.client,
             HTTPStatus.OK),
            (URL_LOGIN, self.client,
             HTTPStatus.OK),
            (URL_LOGOUT, self.client,
             HTTPStatus.OK),
            (URL_SIGNUP, self.client,
             HTTPStatus.OK),
            (URL_NOTES_ADD, self.client,
             HTTPStatus.FOUND),
            (URL_NOTES_LIST, self.client,
             HTTPStatus.FOUND),
            (URL_NOTES_SUCCESS, self.client,
             HTTPStatus.FOUND),
            (URL_NOTES_DETAIL, self.client,
             HTTPStatus.FOUND),
            (URL_NOTES_EDIT, self.client,
             HTTPStatus.FOUND),
            (URL_NOTES_DELETE, self.client,
             HTTPStatus.FOUND),
        ):
            with self.subTest(url=url, user=user):
                self.assertEqual(user.get(url).status_code,
                                 status)

    def test_redirects(self):
        for url, redirect in (
            (URL_NOTES_ADD, REDIRECT_URL_NOTES_ADD),
            (URL_NOTES_LIST, REDIRECT_URL_NOTES_LIST),
            (URL_NOTES_SUCCESS, REDIRECT_URL_NOTES_SUCCESS),
            (URL_NOTES_DETAIL, REDIRECT_URL_NOTES_DETAIL),
            (URL_NOTES_EDIT, REDIRECT_URL_NOTES_EDIT),
            (URL_NOTES_DELETE, REDIRECT_URL_NOTES_DELETE),
        ):
            user = self.client
            with self.subTest(url=url, user=user):
                self.assertRedirects(
                    user.get(url),
                    redirect,
                )

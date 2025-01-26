import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_home_news_count(client, home_url, news_list):
    response = client.get(home_url)
    new_item = response.context.get('object_list', [])
    news_count = new_item.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_home_news_order(client,
                         home_url,
                         news_list):
    response = client.get(home_url)
    new_item = response.context.get('object_list', [])
    all_dates = [news.date for news in new_item]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_detail_comments_order(client,
                               comments_list,
                               detail_url):
    response = client.get(detail_url)

    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    comments_data_list = [comment.created for comment in all_comments]
    sorted_comments_data_list = sorted(comments_data_list)
    assert comments_data_list == sorted_comments_data_list


@pytest.mark.django_db
def test_anonymous_client_dont_has_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(auth_client, detail_url):
    response = auth_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)

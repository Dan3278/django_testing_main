from django.conf import settings
from news.forms import CommentForm


def test_news_count(client, lot_news, url_home):
    assert (
        client.get(url_home).context['object_list'].count()
        == settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(client, lot_news, url_home):
    all_dates = [
        news.date for news in
        client.get(url_home).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news, lot_comments,
                        detail_news_url
                        ):
    assert 'news' in client.get(detail_news_url).context
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in
                      all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client,
                                      detail_news_url):
    assert 'form' not in client.get(detail_news_url).context


def test_authorized_client_has_form(admin_client,
                                    detail_news_url):
    assert isinstance(
        admin_client.get(detail_news_url).context.get('form'),
        CommentForm
    )

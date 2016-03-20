from bson import ObjectId

from crawler.serializers import payload_serializer
from crawler.worker.base import BaseSite


def test_base_site_crawling(mongodb):
    base = BaseSite()
    page = 1
    host = 'http://clien.net/cs2/bbs/board.php'
    query = 'bo_table=park&page={}'.format(page)
    clien_url = '{host}?{query}'.format(host=host, query=query)
    r = base.crawling(clien_url)
    assert r


def test_base_site_insert_or_update(mongodb):
    base = BaseSite()
    obj = payload_serializer(type='test', id=1234, link='test.com', count=1,
                             title='test_title')
    r = base.insert_or_update(obj)
    assert r
    assert isinstance(r, ObjectId)

    document = 'archive'
    obj = base.db.query(document).find_one({'_id': r})
    assert obj['_id'] == r
    assert obj['title'] == 'test_title'
    assert obj['type'] == 'test'
    assert obj['id'] == 1234
    assert obj['link'] == 'test.com'
    assert obj['count'] == 1

    obj = payload_serializer(type='test', id=1234, link='test.com', count=99,
                             title='test_title')
    r = base.insert_or_update(obj)
    obj = base.db.query(document).find_one({'_id': r})
    assert obj['_id'] == r
    assert obj['title'] == 'test_title'
    assert obj['type'] == 'test'
    assert obj['id'] == 1234
    assert obj['link'] == 'test.com'
    assert obj['count'] == 99

from crawler.serializers import payload_serializer


def test_payload_serializer():
    obj = payload_serializer(type='test', id=1234, link='test.com', count=99,
                             title='test_title')
    assert obj['title'] == 'test_title'
    assert obj['type'] == 'test'
    assert obj['id'] == 1234
    assert obj['link'] == 'test.com'
    assert obj['count'] == 99


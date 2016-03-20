from bson import ObjectId

from crawler.database import MongoDB


def test_insert():
    db = MongoDB('test')
    doc = 'test'
    data = {'test': 123}
    r = db.insert(doc, data=data)
    assert r
    assert isinstance(r, ObjectId)
    c = db.query(doc) \
        .find_one({'_id': r})
    assert c['test'] == 123


def test_query():
    db = MongoDB('test')
    doc = 'test'
    r = db.query(doc)
    assert r
    assert r == db.collection[doc]


def test_update():
    db = MongoDB('test')
    doc = 'test'
    data = {'test': 123}
    db.insert(doc, data=data)
    c = db.query(doc) \
        .find_one({'test': 123})
    r = db.update(doc, c=c, data={'test': 999})
    assert r['ok'] == True
    c2 = db.query(doc) \
        .find_one({'_id': c['_id']})
    assert c2['test'] == 999

from unittest import mock

import pytest
from pytest_dbfixtures import factories

mongo_proc = factories.mongo_proc(executable='/usr/local/bin/mongod',
                                  params='--nojournal --noauth '
                                         '--nohttpinterface --noprealloc')
test_mongodb = factories.mongodb('mongo_proc')


@pytest.yield_fixture(autouse=True)
def fx_database(test_mongodb):
    with mock.patch(
            'crawler.database.MongoClient',
            return_value=test_mongodb):
        yield test_mongodb

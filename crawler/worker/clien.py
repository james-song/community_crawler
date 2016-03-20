""":mod:`crawler.worker.clien` ---  Crawler for Clien
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer

logger = logging.getLogger(__name__)


class Clien(BaseSite):

    def __init__(self, *, threshold=20, page_max=20):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.page_max = page_max

    def crawler(self):
        l = logger.getChild('Clien.crawler')
        for page in range(1, self.page_max, 1):
            host = 'http://clien.net/cs2/bbs/board.php'
            query = 'bo_table=park&page={}'.format(page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def do(self):
        l = logger.getChild('Clien.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            for ctx in soup.select('tr.mytr'):
                _temp = ctx.select('td.post_subject span')
                if len(_temp) != 0 and \
                        int(_temp[0].text[1:-1]) >= self.threshold:
                    _id = ctx.select('td')[0].text
                    _count = _temp[0].text[1:-1]
                    _title = ctx.select('td.post_subject a')[0].text
                    _link = self.url.split('?')[0] + '?' + ctx.select('a')[0] \
                        .get('href') \
                        .split('?')[1]
                    obj = payload_serializer(type=self.type, id=_id,
                                             link=_link, count=_count,
                                             title=_title)
                    self.insert_or_update(obj)

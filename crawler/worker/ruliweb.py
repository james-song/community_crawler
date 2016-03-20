""":mod:`crawler.worker.ruliweb` ---  Crawler for Ruliweb
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer

logger = logging.getLogger(__name__)


class Ruliweb(BaseSite):

    def __init__(self, *, threshold=15, page_max=20):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.pageMax = page_max

    def crawler(self):
        l = logger.getChild('Ruliweb.crawler')
        for page in range(1, self.pageMax, 1):
            host = 'http://bbs2.ruliweb.daum.net/gaia/do/ruliweb/default' \
                   '/community/2078/list'
            query = 'bbsId=G005&pageIndex={}'.format(page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def do(self):
        l = logger.getChild('Ruliweb.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            for ctx in soup.select('tbody tr'):
                _temp = ctx.select('span.num_reply span.num')
                if len(_temp) != 0 and \
                        int(_temp[0].text) >= self.threshold:
                    _id = ctx.select('a')[1].get('id').split('_')[1]
                    _count = _temp[0].text
                    _title = ctx.select('a')[1].text
                    _link = self.url.split('list?')[0] + ctx \
                        .select('a')[1] \
                        .get('href')
                    obj = payload_serializer(type=self.type, id=_id,
                                             link=_link, count=_count,
                                             title=_title)
                    self.insert_or_update(obj)

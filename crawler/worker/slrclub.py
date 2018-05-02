""":mod:`crawler.worker.slrclub` ---  Crawler for Slrclub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer

logger = logging.getLogger(__name__)


class Slrclub(BaseSite):

    def __init__(self, *, threshold=15, page_max=20):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.pageMax = page_max

    def crawler(self):
        l = logger.getChild('Slrclub.crawler')
        for page in range(1, self.pageMax, 1):
            host = 'http://www.slrclub.com/bbs/zboard.php'
            query = 'id=free&page={}'.format(page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def do(self):
        l = logger.getChild('Slrclub.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            for ctx in soup.select('table#bbs_list tbody tr'):
                if ctx.select('td.list_num'):
                    text = ctx.a.extract()
                    _temp = ctx.select('td.sbj')[0].text.strip()
                    if _temp != '' and int(_temp[1:-1]) >= self.threshold:
                        _id = text.get('href').split('no=')[1]
                        _count = _temp[1:-1]
                        _title = text.text
                        _link = self.url.split('/bbs')[0] + \
                            text.get('href')
                        obj = payload_serializer(type=self.type, id=_id,
                                                 link=_link, count=_count,
                                                 title=_title)
                        self.insert_or_update(obj)

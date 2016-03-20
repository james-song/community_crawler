""":mod:`crawler.worker.todayhumor` ---  Crawler for TodayHumor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from .base import BaseSite
from ..exc import SkipCrawler
from ..serializers import payload_serializer

logger = logging.getLogger(__name__)


class Todayhumor(BaseSite):

    def __init__(self, *, threshold=100, page_max=5):
        BaseSite.__init__(self)
        self.threshold = threshold
        self.pageMax = page_max

    def crawler(self):
        l = logger.getChild('Todayhumor.crawler')
        for page in range(1, self.pageMax, 1):
            host = 'http://www.todayhumor.co.kr/board/list.php'
            query = 'table=bestofbest&page={}'.format(page)
            self.url = '{host}?{query}'.format(host=host, query=query)
            soup = self.crawling(self.url)
            if soup is None:
                l.error('{} crawler skip'.format(self.type))
                raise SkipCrawler
            yield soup

    def do(self):
        l = logger.getChild('Todayhumor.do')
        l.info('start {} crawler'.format(self.type))
        for soup in self.crawler():
            for ctx in soup.select('td.subject'):
                _temp = ctx.select('span')
                if len(_temp) != 0 and \
                        int(_temp[0].text[2:-1]) >= self.threshold:
                    _id = ctx.select('a')[0] \
                        .get('href') \
                        .split('s_no=')[1] \
                        .split('&page')[0]
                    _count = _temp[0].text[2:-1]
                    _title = ctx.select('a')[0].text
                    _link = self.url.split('/board/list.php')[0] + ctx \
                        .select('a')[0] \
                        .get('href')
                    obj = payload_serializer(type=self.type, id=_id,
                                             link=_link, count=_count,
                                             title=_title)
                    self.insert_or_update(obj)

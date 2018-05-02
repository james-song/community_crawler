""":mod:`crawler.serve` ---  Crawler thread context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging.config
import random
import threading

from datetime import datetime, timedelta

from queue import Queue

from crawler.config import crawler_config
from crawler.exc import SkipCrawler, TerminatedCrawler
from crawler.worker.clien import Clien
from crawler.worker.ppomppu import Ppomppu
from crawler.worker.ruliweb_hobby import RuliwebHobby
from crawler.worker.ruliweb_hotdeal import RuliwebHotdeal
from crawler.worker.ruliweb_humor import RuliwebHumor
from crawler.worker.slrclub import Slrclub
from crawler.worker.todayhumor import Todayhumor

from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger('crawler')
logging.config.dictConfig(crawler_config.logging_formatter)


class Crawler(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.is_stop = False
        self.queue = queue

    def run(self):
        l = logger.getChild('Crawler.run')
        site = self.queue.get()

        try:
            site.do()
        except ServerSelectionTimeoutError:
            l.error('TimeOut Error %s', site)
        except SkipCrawler:
            l.info('Crawler Skip')
        except:
            l.error('Unhandled Exception')
        self.queue.task_done()


def crawler(*, queue: Queue):
    sites = [
        Clien(threshold=20, page_max=10),
        Ppomppu(threshold=30, page_max=10),
        Slrclub(threshold=15, page_max=10),
        Todayhumor(threshold=20, page_max=10),
        RuliwebHobby(threshold=15, page_max=10),
        RuliwebHumor(threshold=15, page_max=10),
        RuliwebHotdeal(threshold=15, page_max=10),
    ]
    thread_num = len(sites)
    for site in sites:
        queue.put(site)
    workers = []
    for i in range(thread_num):
        t = Crawler(queue)
        t.daemon = True
        workers.append(t)
        t.start()
    return workers


if __name__ == '__main__':
    l = logger.getChild('main')
    oldtime = datetime.now()
    l.info('crawler start')
    count = 0
    queue = Queue()
    while True:
        try:
            interval = crawler_config.crawler_interval
            seed = timedelta(minutes=random.randint(
                int(interval['minutes_min']), int(interval['minutes_max'])),
                seconds=int(interval['sec']))
            if datetime.now() >= (oldtime + seed):
                oldtime = datetime.now()
                workers = crawler(queue=queue)
                queue.join()
                count += 1
                l.info("finish crawler: {}".format(count))
        except (KeyboardInterrupt, TerminatedCrawler):
            l.info('terminated crawler')
            exit()

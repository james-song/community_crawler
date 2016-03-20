""":mod:`crawler.exc` ---  Crawler Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class TerminatedCrawler(RuntimeError):
    pass


class SkipCrawler(ValueError):
    pass

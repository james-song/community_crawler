""":mod:`crawler.serializers` ---  Serializer for crawler data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime
import time


def payload_serializer(*, type: str, id: int, link: str, count: int,
                       title: str) -> dict:
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    return {'type': type,
            'id': id,
            'link': link,
            'count': count,
            'title': title,
            'date': utc_now.isoformat()
            }

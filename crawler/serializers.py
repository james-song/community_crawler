""":mod:`crawler.serializers` ---  Serializer for crawler data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime


def payload_serializer(*, type: str, id: int = None, link: str, count: int,
                       title: str) -> dict:
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    dic = {'type': type,
            'link': link,
            'count': count,
            'title': title,
            'date': utc_now.isoformat()
            }
    
    dic['id'] = id
    return dic

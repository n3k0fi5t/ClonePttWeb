from http import HTTPStatus

import requests
from requests import HTTPError, ConnectionError
from celery import shared_task

from post.models import Board
from crawl.models import Crawler

from crawl.PttSpider.PttSpider import PttUrl

def board_url(name):
    return PttUrl.urlify(name)

def validate_board_by_url(url):
    result = True

    try:
        rs = requests.get(url)
        rs.raise_for_status()

        if rs.status_code != HTTPStatus.OK:
            result = False
    except HTTPError as e:
        result = False
    except ConnectionError as e:
        result = False
    
    return result

def validate_board_name(name):
    result = True

    if name == "":
        result = False

    if not validate_board_by_url(board_url(name)):
        result = False

    return result

@shared_task
def add_board(board_name):
    if not validate_board_name(board_name):
        return
    
    if Board.objects.filter(name=board_name).exists():
        return
    
    obj = Board.objects.create(
        name=board_name,
        url=board_url(board_name),
    )

    # create corresponding crawler data
    Crawler.objects.create(board=obj)


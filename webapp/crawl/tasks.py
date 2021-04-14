import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256

import requests

from celery import shared_task

from logging import getLogger
log = getLogger()

from webapp import celery_app
from post.models import (
    Board,
    Post,
    Push,
    URLImage
)

from .models import Crawler, CrawlerStatus

from .PttSpider import PttSpider as Spider

@shared_task
def update_article(board, article_url, rs=None):
    def hash_content(ctx):
        hash = sha256()
        hash.update(bytes(ctx, 'utf-8'))
        return hash.hexdigest()

    if not isinstance(board, Board):
        try:
            board = Board.objects.get(name=board)
        except Board.DoesNotExist:
            log.warn(f"{board} not exist")
            return

    spider = Spider.PttArticleSpider(url=article_url, rs=rs)
    spider.run()

    article = spider.article
    defaults = {
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'endpoint': article.url.endpoint,
            'image_url': article.image_urls[0] if len(article.image_urls) else "",
            'board': board,
    }

    post, created = Post.objects.get_or_create(
            endpoint=article.url.endpoint,
            defaults=defaults
    )

    # check content should be updated
    if not created:
        old_hash = hash_content(post.content)
        new_hash = hash_content(article.content)

        if old_hash != new_hash:
            post.content = article.content
            post.save()

    if post and len(article.push_list):
        push_list = []

        def is_same_push(p1, p2):
            if p1.name != p2.name:
                return False
            elif p1.content != p2.content:
                return False
            elif p1.type != p2.type:
                return False
            return True

        db_push_list = Push.objects.filter(post=post)
        for article_push in article.push_list:
            need_update = True
            for db_push in db_push_list:
                if is_same_push(db_push, article_push):
                    need_update = False
            
            if need_update:
                push_list.append(article_push)

        Push.objects.bulk_create(
            [Push(
                name=push.name,
                type=push.type,
                content=push.content,
                ipdatetime=push.date,
                post=post,
            ) for push in push_list]
        )

    # only update relative image url when first create post
    if created and len(article.image_urls):
        URLImage.objects.bulk_create(
            [URLImage(url=url) for url in article.image_urls]
        )

@shared_task
def batch_update(board_name, url_list):
    rs = requests.session()
    board = Board.objects.get(name=board_name)
    for url in url_list:
        update_article(board, url, rs=rs)

@shared_task
def crawl_board(name, last_update_page):
    # get board information first
    try:
        board = Board.objects.get(name=name)
    except Board.DoesNotExist:
        return

    url = board.url
    rs = requests.session()
    board_spider = Spider.PttArticleListSpider(url, rs=rs, last_page=last_update_page, max_fetch=1000)
    board_spider.run()

    article_urls = board_spider.article_url_list[::-1]

    batch_size = len(article_urls)
    if batch_size != 0:
        for idx in range(0, len(article_urls), batch_size):
            batch_update.apply_async((board.name, article_urls[idx:idx+batch_size]), queue='period', routing_key='crawl.update')

    return board_spider.latest_idx

def update_crawler_status(obj, status, last_update=0):
    obj.status = status
    if last_update > 0:
        obj.last_update_page = last_update
    obj.save()

@celery_app.task
def period_crawl_task(board_name, last_update_page):
    from time import sleep
    from random import randint

    # random delay
    sleep(randint(5, 30))

    # get board information first
    try:
        board = Board.objects.get(name=board_name)
    except Board.DoesNotExist:
        return

    obj, _ = Crawler.objects.get_or_create(
        board=board,
        defaults={'board': board}
    )

    try:
        # crawling task may takes much time inducing status false recognize, so we update early and later
        update_crawler_status(obj, CrawlerStatus.NORMAL)
        latest_idx = crawl_board(board_name, last_update_page)
        update_crawler_status(obj, CrawlerStatus.NORMAL, last_update=latest_idx)
    except Exception as e:
        log.warn(e)
        update_crawler_status(obj, CrawlerStatus.ERROR)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    crawler_list = Crawler.objects.select_related('board').all()
    for crawler in crawler_list:
        sender.add_periodic_task(
            300,
            period_crawl_task.s(crawler.board.name, crawler.last_update_page),
        )

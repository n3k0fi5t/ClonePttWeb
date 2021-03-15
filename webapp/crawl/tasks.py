
from celery import shared_task

from webapp import celery_app
from post.models import (
    Board,
    Post,
    URLImage
)

from .models import Crawler, CrawlerStatus

from .PttSpider import PttSpider as Spider

@shared_task
def crawl_board(name):
    # get board information first
    try:
        board = Board.objects.get(name=name)
    except Board.DoesNotExist:
        return

    url = board.url
    rs = Spider.RequestWrapper()
    board_spider = Spider.PttArticleListSpider(url, rs=rs, max_fetch=20)
    board_spider.run()

    article_urls = board_spider.article_url_list[::-1]
    spiders = (Spider.PttArticleSpider(url, rs=rs) for url in article_urls)

    for spider in spiders:
        # already crawled, we can skip rest
        if Post.objects.filter(endpoint=spider.url.endpoint).exists():
            continue
        spider.run()

        article = spider.article

        post = Post.objects.get_or_create(
                endpoint=article.url.endpoint,
                defaults={
                    'title': article.title,
                    'content': article.content,
                    'author': article.author,
                    'endpoint': article.url.endpoint,
                    'image_url': article.image_urls[0] if len(article.image_urls) else "",
                    'board': board
        })

        if post and len(article.image_urls):
            URLImage.objects.bulk_create(
                [URLImage(url=url) for url in article.image_urls]
            )

def update_crawler_status(obj, status):
    obj.status = status
    obj.save()

@celery_app.task
def board_crawl_task(board_name):
    from time import sleep
    from random import randint

    # random delay
    sleep(randint(5, 30))

    # get board information first
    try:
        board = Board.objects.get(name=board_name)
    except Board.DoesNotExist:
        return

    obj, created = Crawler.objects.get_or_create(
        board=board,
        defaults={'board': board}
    )

    try:
        update_crawler_status(obj, CrawlerStatus.NORMAL)
        crawl_board(board_name)
        update_crawler_status(obj, CrawlerStatus.NORMAL)
    except Exception as e:
        update_crawler_status(obj, CrawlerStatus.ERROR)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    board_list = Board.objects.all().values_list('name', flat=True)
    for board in board_list:
        sender.add_periodic_task(299, board_crawl_task.s(board))
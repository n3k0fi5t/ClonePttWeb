import datetime

from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone

from crawl import CrawlerStatus

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    url = models.TextField(blank=False)

    @property
    def status(self):
        stat = self.crawler.status

        if stat != CrawlerStatus.NORMAL:
            return stat

        delta = (timezone.now() - self.crawler.last_update).total_seconds()
        if delta > 500:
            stat = CrawlerStatus.ERROR

        return stat

    class Meta:
        db_table = 'ptt_board'


class Post(models.Model):
    title = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=True)
    endpoint = models.TextField(blank=True)

    image_url = models.TextField(blank=True)

    create_time = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    class Meta:
        ordering = ['create_time']
        db_table = 'ptt_post'


class URLImage(models.Model):
    url = models.TextField(blank=False)

    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create_time']
        db_table = 'image_url'
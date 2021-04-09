import datetime
from django import conf

from django.conf import settings
from django.contrib.postgres import indexes
from django.db import models
from django.db.models import fields
from django.db.models.enums import Choices
from django.db.models.fields import DateTimeField
from django.utils import timezone

from django.contrib.postgres.search import SearchQuery, SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex

from crawl import (
    CrawlerStatus,
    Spider
)

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
        indexes = [
            models.Index(fields=['id', 'name']),
        ]


class PostManager(models.Manager):
    def search(self, keywords, *args, **kwargs):
        # generate ts query
        query_kw = '|'.join(keywords)
        query = SearchQuery(query_kw, config=settings.SEARCH_CONFIG)

        # generate ts vector
        #ts = SearchVector('title', 'content', config=settings.SEARCH_CONFIG)
        #return super(PostManager, self).annotate(search=ts).filter(search=query)
        return super(PostManager, self).filter(tsvector=query)

class Post(models.Model):
    title = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=True)
    endpoint = models.TextField(blank=True)
    image_url = models.TextField(blank=True)

    create_time = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    tsvector = SearchVectorField(blank=True, null=True)

    objects = PostManager()
    class Meta:
        ordering = ['-create_time']
        db_table = 'ptt_post'
        indexes = [
            models.Index(fields=['endpoint']),
            models.Index(fields=['board', 'create_time']),
            GinIndex(fields=['tsvector']),
        ]

class URLImage(models.Model):
    url = models.TextField(blank=False)

    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create_time']
        db_table = 'image_url'


PUSH_TYPE_CHOICES = (
    (Spider.PushType.ARROW, u'→'),
    (Spider.PushType.DOWN, u'噓 '),
    (Spider.PushType.UP, u'推 '),
)

class Push(models.Model):
    name = models.CharField(max_length=50, blank=False)
    type = models.IntegerField(choices=PUSH_TYPE_CHOICES)
    content = models.TextField()

    ipdatetime = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @property
    def type_string(self):
        return PUSH_TYPE_CHOICES[self.type][1]
    class Meta:
        db_table = 'push'
        ordering = ['create_time']
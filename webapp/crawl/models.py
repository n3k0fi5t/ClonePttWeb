from django.db import models
from django.db.models.base import Model
from post.models import Board
from . import CrawlerStatus

# Create your models here.
class Crawler(models.Model):
    status = models.IntegerField(blank=False, default=CrawlerStatus.ERROR)
    last_update = models.DateTimeField(auto_now=True)

    board = models.OneToOneField(Board, on_delete=models.CASCADE, primary_key=True)
    last_update_page = models.IntegerField(blank=False, default=1)

    class Meta:
        db_table = 'crawler'

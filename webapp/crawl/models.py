from django.db import models
from post.models import Board
from . import CrawlerStatus

# Create your models here.
class Crawler(models.Model):
    status = models.IntegerField(blank=False, default=CrawlerStatus.ERROR)
    last_update = models.DateTimeField(auto_now=True)

    board = models.OneToOneField(Board, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'crawler'

from .PttSpider.PttSpider import ptt_spider as Spider

class CrawlerStatus:
    NORMAL = 0
    ERROR = 1


__all__ = ['CrawlerStatus', 'Spider']
from django.shortcuts import render, redirect
from django.urls import reverse

from crawl.tasks import period_crawl_task
from crawl.models import Crawler
from post.models import Board, Post

from utils.paginate import paginate
from utils.response import http_response_data
from utils.request_params import param2str

class Action(object):
    @classmethod
    def browse(cls, request, **kwargs):
        board_name = param2str(request, 'POST', 'board_name', "")
        return redirect(reverse('post:board', args=(board_name, )))

    @classmethod
    def default(cls, request, **kwargs):
        return redirect(reverse('home:home'))

    @classmethod
    def crawl(cls, request, **kwargs):
        board_name = param2str(request, 'POST', 'board_name', "")
        crawler = Crawler.objects.get(board__name=board_name)
        period_crawl_task.apply_async(
            (board_name, crawler.last_update_page),
            queue='web',
            routing_key='app.for_test'
        )

        return redirect(reverse('home:home'))

    @classmethod
    def search(cls, request, **kwargs):
        keyword = param2str(request, 'GET', 'search', "")
        search_keywords = keyword.split()
        qs = Post.objects.search(search_keywords).select_related('board')

        board_name = param2str(request, 'GET', 'board_name', "")
        if board_name != "":
            qs = qs.filter(board__name__iexact=board_name)

        paged_objs, count, page, limit = paginate(qs, request, limit_defval=5)

        data = http_response_data(
            request,
            **{
                'board_name': "",
                'post_list': paged_objs,
                'page': page,
                'limit': limit,
                'count': count
            }
        )
        return render(request, 'board.html', data)
    
    @classmethod
    def get(cls, action_name):
        action = cls.default

        if isinstance(action_name, str):
            action = getattr(cls, action_name, cls.default)

        return action
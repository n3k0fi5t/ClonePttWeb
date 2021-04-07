from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .tasks import add_board
from .actions import Action

from crawl.tasks import period_crawl_task
from crawl.models import Crawler
from post.models import Board, Post

from utils.paginate import paginate
from utils.response import http_response_data
from utils.request_params import param2str

# Create your views here.
class HomeView(View):
    def render_home(self, request):
        qs = Board.objects.select_related('crawler').all()
        paged_objs, count, page, limit = paginate(qs, request, limit_defval=5)

        data = http_response_data(
            request,
            **{
                'board_list': paged_objs,
                'page': page,
                'limit': limit,
                'count': count,
            }
        )

        return render(request, 'home.html', data)

    def get(self, request):
        return self.render_home(request)

    def post(self, request):
        """ should be moved to actions
        """
        args = request.POST or None
        board_name = args.get('board', "")

        add_board.delay(board_name)
        return self.render_home(request)

class HomeActionView(View):
    def get(self, request):
        action = 'default'

        search = param2str(request, 'GET', 'search', "")
        if search != "":
            action = 'search'

        handler = Action.get(action)
        return handler(request)

    def post(self, request):
        action = param2str(request, 'POST', 'action', 'default')

        handler = Action.get(action)
        return handler(request)


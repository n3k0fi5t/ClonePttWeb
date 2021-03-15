from .request_params import param2int

def paginate(qs, request, limit_defval=10, page_defval=1):
    """ paginate queryset
        queryset will be divided into groups with at most "limit" elements

    Args:
        qs: queried QuerySet
        request: HttpRequest instance
        limit_defval: default value of limit
        page_defval: default value of page 

    Returns:
        qs: paginated QuerySet
        count: number of element of original queryset
        page: current page
        limit: current limit

    """
    limit = param2int(request, 'get', 'limit', limit_defval)
    if limit < 0 or limit > 50:
        limit = 10
    
    page = param2int(request, 'get', 'page', page_defval)
    if page < 1:
        page = 1

    count = qs.count()
    
    return qs[(page-1)*limit:page*limit], count, page, limit
from urllib import parse

def request2crumb(request):
    """generate breadcrumb

    Args:
        request: HttpRequest instance
    
    Returns:
        crumb: name-path pair dictionary

    """

    # name: crumb
    crumb = {}

    try:
        url = request.path
    except Exception:
        return crumb

    parse_res = parse.urlparse(url)

    # home
    cur_path = "/"
    crumb["Home"] = cur_path

    for path in parse_res.path.split('/'):
        if path:
            cur_path += path + "/"
            crumb[path] = cur_path

    return crumb
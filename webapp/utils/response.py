from .breadcrumb import request2crumb

def http_response_data(request, **kwargs):
    """generate response data for http response
    
    Args:
        request: HttpRequest instance
        kwargs: key-value arguments to be responsed

    Returns:
        data: k-v pair of data

    """
    data = {}
    
    data.update(kwargs)

    # breadcrumb
    data['breadcrumb'] = request2crumb(request)

    return data
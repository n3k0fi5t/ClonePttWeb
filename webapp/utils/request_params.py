def param2type(request, method, param, data_type, defval=None):
    """ get http request paramter

    Args:
        request: HttpRequest instance
        method: string of HTTP method
        param: string of parameter
        data_type: type of parameter
        defval: default value if parameter do not exist in request method
    
    Returns:
        val: parameter value
    
    """
    method = method.upper()

    try:
        val = data_type(getattr(request, method).get(param, defval))
    except ValueError:
        val = defval
    except Exception as e:
        val = defval
    
    return val

def param2int(request, method, param, defval=0):
    return param2type(request, method, param, int, defval=defval)

def param2str(request, method, param, defval=""):
    return param2type(request, method, param, str, defval=defval)

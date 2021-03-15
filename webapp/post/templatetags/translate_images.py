import re

from django import template

register = template.Library()

def url2imghtml(url):
    return f'<img src="{url}" class="img-thumbnail col-sm-6">'

@register.filter
def translateimg(value):
    def is_image_url(url):
        regex = re.compile(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|bmp|jpeg|gif)')

        if regex.match(url):
            return True
        return False
    out = []
    for line in value.split('\n'):
        if is_image_url(line):
            out.append(url2imghtml(line))
        else:
            out.append(line)
    
    return '\n'.join(out)

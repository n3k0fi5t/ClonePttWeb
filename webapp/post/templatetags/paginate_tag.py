from django import template

register = template.Library()

class HtmlElement:
    def __init__(self, tag, tag_val="", **attrs):
        self.tag = tag
        self.tag_val = str(tag_val)
        self.attrs = attrs
        self._subtags = []

    def add_subtag(self, subtag):
        if isinstance(subtag, HtmlElement):
            self._subtags.append(subtag)

    def add_attr(self, name, value):
        self.attrs[name] = self.attrs.get(name, "") + " " + value

    def _open_arrow(self):
        html = f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items())
        html += '>\n'

        return html

    def _close_arrow(self):
        html = f'</{self.tag}>\n'

        return html

    def __str__(self):
        repr = self._open_arrow()
        for subtag in self._subtags:
            repr += str(subtag)
        repr += self.tag_val
        repr += self._close_arrow()

        return repr


def paged_url(url, page=0, **attr):
    url += f"?page={page}&"
    for k, v in attr.items():
        url += f"{k}={v}&"
    
    if url[-1] == '&':
        url = url[:-1]
    return url

def page_item(idx, url, **page_attr):
    if idx < 1:
        return HtmlElement('div')
    item = HtmlElement('li', **{'class': 'page-item'})
    item.add_subtag(HtmlElement('a', idx, **{'class': 'page-link', 'href':paged_url(url, idx, **page_attr)}))

    return item

GAP = 3
CONSECUTIVE = 2

@register.simple_tag
def pagination(url, total, limit, page):
    """ generate html pagination elements

    Args:
        url: url of resource
        total: number of elements
        limit: number of element in a page
        page: current page number

    Returns:
        result: string of html pagination element

    """
    page_attr = {'limit': limit}
    cur = page

    max_page = (total-1)//limit
    cur -= 1 # map to index
    if cur > max_page:
        cur = max_page
    if cur < 0:
        cur = 0

    pg = HtmlElement('ul', **{'class': 'pagination'})

    # handle "<"
    prev = HtmlElement('li', **{'class': 'page-item'})

    a = HtmlElement('a', **{'class': 'page-link', 'href':paged_url(url, cur, **page_attr), 'aria-label':'Previous', 'tabindex': cur-1})
    a.add_subtag(HtmlElement('span', "&laquo;", **{'aria-hidden': 'true'}))
    a.add_subtag(HtmlElement('span', **{'class': 'sr-only'}))
    if cur -1 < 0:
        prev.add_attr('class', 'disabled')

    prev.add_subtag(a)
    pg.add_subtag(prev)
    
    # ...
    if cur != 0:
        pg.add_subtag(page_item(1, url, **page_attr))

        if cur-GAP > 0:
            item = HtmlElement('li', **{'class': 'page-item'})
            item.add_subtag(HtmlElement('a', "⋯⋯", **{'class': 'page-link', 'href':paged_url('#', 0, **page_attr)}))
            pg.add_subtag(item)

    # left pages
    for idx in range(cur-1, cur-CONSECUTIVE-1, -1)[::-1]:
        if 1 <= idx <= max_page:
            pg.add_subtag(page_item(idx+1, url, **page_attr))

    # current page
    item = page_item(cur+1, url, **page_attr)
    item.add_attr('class', 'active')
    pg.add_subtag(item)

    for idx in range(cur+1, cur+CONSECUTIVE+1):
        if 1 <= idx < max_page:
            pg.add_subtag(page_item(idx+1, url, **page_attr))

    # ...
    if cur != max_page:
        if cur+GAP < max_page:
            item = HtmlElement('li', **{'class': 'page-item'})
            item.add_subtag(HtmlElement('a', "⋯⋯", **{'class': 'page-link', 'href':paged_url('#', 0, **page_attr)}))
            pg.add_subtag(item)

        pg.add_subtag(page_item(max_page+1, url, **page_attr))
    
    # handle ">"
    prev = HtmlElement('li', **{'class': 'page-item'})

    a = HtmlElement('a', **{'class': 'page-link', 'href':paged_url(url, cur+2, **page_attr), 'aria-label':'Next', 'tabindex': -1 if cur+1 > max_page else cur+1})
    a.add_subtag(HtmlElement('span', "&raquo;", **{'aria-hidden': 'true'}))
    a.add_subtag(HtmlElement('span', **{'class': 'sr-only'}))
    if cur + 1 > max_page:
        prev.add_attr('class', 'disabled')

    prev.add_subtag(a)
    pg.add_subtag(prev)

    return str(pg)
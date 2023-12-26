from __future__ import annotations

from hx_markup.element import Element
from spacestar import CSS_HEAD_BUBLES, SCRIPT_BODY_BUBLES


def init_element(tag, /, *args, **kwargs) -> Element:
    booleans = [*args]
    children = kwargs.pop('children', [])
    dataset = kwargs.pop('dataset', {})
    classlist = kwargs.pop('classlist', [])
    styles = kwargs.pop('styles', {})
    htmx = kwargs.pop('htmx', {})
    id = kwargs.pop('id', None)
    for item in booleans[:]:
        if item.startswith('#'):
            if not id:
                id = item[1:]
            booleans.remove(item)
        elif item.startswith('.'):
            classlist.append(item[1:])
            booleans.remove(item)
    return Element(tag, id, booleans, classlist, kwargs, htmx, dataset, styles, children=children)


bootstrap_sript = Element('script', src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        crossorigin="anonymous"
)

bootstrap_link = Element('link', href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        rel="stylesheet",
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        crossorigin="anonymous"
)


def page_head(title: str = None, children: list[Element | str] = None) -> Element:
    head = Element('head', children=[
            Element('meta', charset='utf-8'),
            Element('meta', content="width=device-width, initial-scale=1", name='viewport'),
            Element('title', children=title),
            bootstrap_link,
            CSS_HEAD_BUBLES
            # Element('style', children=[Render.selector_style('*', {'margin': '0', 'padding': '0'}), 'html {background-image: radial_gradient(x1:0, y1:0, x2:x=width, y2:y=height, padding: 0}']),
            # Element('script', src='/static/js/main.js'),
            # Element('link', rel='stylesheet', href='/static/css/main.css'),
    
    ])
    
    if isinstance(children, list):
        head.children.extend(children)
    elif isinstance(children, str):
        head.children.append(children)
    
    return head


def page_body(*args, **kwargs) -> Element:
    children = kwargs.pop('children', [])
    children.append(SCRIPT_BODY_BUBLES)
    return Element('body', *args, children=children, **kwargs)


def page_html(lang: str, title: str, children: list[Element | str] = None) -> Element:
    return Element('html', lang=lang, children=[
            page_head(title),
            page_body('#body', children=children or [Element('h1', children=title)])
    ], before='<!DOCTYPE html>')


def nav_list(children, /, *args, **kwargs) -> Element:
    return init_element('ul', '.navbar-nav', *args, children=children, **kwargs)
 
def nav_item(children: str | Element, *args, **kwargs) -> Element:
    return init_element('li', '.nav-item', *args, children=children, **kwargs)


def nav_link(children: str | Element, href: str, *args, **kwargs) -> Element:
    return init_element('a', '.nav-link', *args, href=href, children=children, **kwargs)


def full_nav_list(data: list[tuple[str, str]]) -> Element:
    links = [nav_link(*i) for i in data]
    return nav_list([nav_item(i) for i in links])


if __name__ == '__main__':
    print(page_html('en', 'spacestar').render())
    print(page_body('#body', children=[Element('h1', children='spacestar')]))
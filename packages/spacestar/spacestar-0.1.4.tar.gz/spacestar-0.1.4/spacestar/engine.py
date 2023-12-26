from __future__ import annotations

import io
import os
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import wraps
from typing import Optional

from hx_markup import Element, functions
from lxml import etree
from lxml.builder import E
from ormspace.alias import QUERIES
from ormspace.model import getmodel
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from spacestar.app import SpaceStar
from spacestar.model import SpaceModel


def add_staticfiles(_app: SpaceStar = None, *, path: str = '/static', directory: str = 'static'):
    def decorator(app):
        @wraps(app)
        def wrapper():
            app.routes.append(
                    Mount(path, app=StaticFiles(directory=os.path.join(os.getcwd(), directory)), name='static'))
            return app
        
        return wrapper()
    
    if _app is None:
        return decorator
    else:
        return decorator(_app)


class ResponseEngine(ABC):
    def __init__(self, request: Request, *args, **kwargs):
        self.request = request
        self.app: SpaceStar = self.request.app
        self.template_path = kwargs.pop('template_path', None)
        self.source = kwargs.pop('source', None)
        self.args = args
        self.kwargs = kwargs
        
    @property
    def engine(self):
        if self.template_path and self.app.templates_directory:
            return self.app.templates.get_template(self.template_path)
        elif self.source:
            return self.app.from_string(self.source)
        return self.app.index
    
    @abstractmethod
    async def data(self) -> dict:
        raise NotImplementedError
    
    async def run(self):
        return self.engine.render(self.request, **await self.data())
    
    # @abstractmethod
    # async def element(self):...
    #
    # async def html(self) -> str:
    #     return etree.tounicode(await self.element(), pretty_print=True)
    #
        
class ModelResponse(ResponseEngine):
    def __init__(self, request: Request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.model = getmodel(self.request.path_params.get('item_name'))

    async def update_dependencies(self, lazy=False, queries: QUERIES | None = None):
        await self.model.update_dependencies_context(queries=queries, lazy=lazy)
    
    @property
    def fields(self):
        return self.model.model_fields.values()
    
    @property
    def query(self):
        result = self.model.query_from_request(request=self.request)
        return result
    
    @property
    def path(self):
        return self.request.url.path
    
    @property
    def field_names(self):
        return self.model.model_fields.keys()
    
    async def instances(self, lazy=False):
        return await self.model.sorted_instances_list(query=self.query, lazy=lazy)

    async def run(self):
        if self.template_path:
            return HTMLResponse(self.app.render(self.request, template=self.template_path, **await self.data()))
        elif self.source:
            return HTMLResponse(self.app.templates.from_string(self.source).render(request=self.request, **await self.data()))
        return self.app.response(self.request, **await self.data())
    
    @classmethod
    async def form_data_dict(cls, request):
        form_data = await request.form()
        base = defaultdict(list)
        for key, value in form_data.items():
            base[key].append(value)
        result = {}
        for key, value in base.items():
            if len(value) == 1:
                result[key] = value[0]
            elif len(value) > 1:
                result[key] = value
        return result
    
def wrap_header(*args, **kwargs):
    return str(Element('div', '#header', children=Element(*args, **kwargs)))
    
class ListResponse(ModelResponse):
    
    async def data(self) -> dict:
        return {
                'header': wrap_header('div', '.container-fluid', children=[Element('h1', children=self.app.title)]),
                'main': etree.tounicode(
                        E.div(
                                E.h2(f'lista de {self.model.plural()}'),
                                E.ul(*[E.li(str(i), {'class': 'list-group-item text-white'}) for i in
                                       await self.instances()],
                                     {'class': 'list-group', 'style': 'overflow-y: auto; max-height: 80%;'})
                        
                        )
                        
                ),
                'footer': etree.tounicode(E.footer(f'resultados para {functions.write_args(self.query.values())}', id='footer'))
        }
    
    # async def element(self) -> etree.Element:
    #     page = E.div(
    #                     E.h4('lista de {}'.format(self.model.plural()).title()),
    #                     E.ul(
    #                             *[E.li(str(i), {'class': 'list-group-item',
    #                                             'style': 'background-color: transparent; color: white'}) for i in
    #                               await self.model.sorted_instances_list(lazy=False, query=self.model.query_from_request(self.request))],
    #                             id='{}-list'.format(self.model.item_name()),
    #                             **{'class': 'list-group'},
    #                             style='overflow-y: auto; max-height: 75vh;'
    #                     ),
    #                     style='display: grid; justify-content: center;'
    #             )
    #     return page
        

class SearchResponse(ModelResponse):
    async def element(self):
        page = E.div(
                E.h4('resultado de pesquisa de {}'.format(self.model).title()),
        )
        return page
    

def list_component_route(_model: type[SpaceModel] = None):

    def wrapper(model: type[SpaceModel]):
        @wraps(model)
        def wrapped():
            async def list_component_endpoint(request: Request):
                return request.app.response(request,
                                            model=model,
                                            instances=model.sorted_instances_list(query={**request.query_params}),
                                            template=f'component/list.html')
            return list_component_endpoint
        model._list_component_route = wrapped()
        return model
    if _model:
        return wrapper(_model)
    return wrapper
                # with io.StringIO() as f:
                #     container = init_element('div', f'#{model.item_name()}__list__container .card-box')
                #     container.children.append(init_element('h3', children=f'Lista de {model.plural()}'))
                #     group = init_element('ul', 'nav')
                #     for item in items:
                #         group.children.append(init_element('li', f'#{model.item_name()}__{item.key} .nav-item'))
                #     container.children.append(group)
                #     f.write(str(container))
                #     text = f.getvalue()
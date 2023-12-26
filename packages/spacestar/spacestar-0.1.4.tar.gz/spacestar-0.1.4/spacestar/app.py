from __future__ import annotations

import os.path
from functools import wraps
from typing import Optional

import jinja2
import uvicorn
from lxml import etree
from lxml.builder import E
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from spacestar import component as cp, spacestar_settings, templates as tp
from spacestar.middleware import session_middleware
from spacestar.templates import app_context


class SpaceStar(Starlette):
    """SpaceStar class is a mix of Starlette and Uvicorn for faster run of HTTP server configured for Deta Space.
    Parameters:
    module - A string with the module name running the application. Defaults to "main".
    app_name - A string with the SpaceStar instance name. Defaults to "app".
    lang - Language of the application. Defaults to "en".
    title - The title for home page. Defaults to "SpaceStar".
    static_directory - A string indicating the location of static folder, relative to working directory.
    templates_directory - A string indicating the location of jinja2 templates_directory.
    debug - Boolean indicating if debug tracebacks should be returned on errors.
    routes - A list of routes to serve incoming HTTP and WebSocket requests.
    middleware - A list of middleware to run for every request. A starlette application will always automatically include two middleware classes. ServerErrorMiddleware is added as the very outermost middleware, to handle any uncaught errors occurring anywhere in the entire stack. ExceptionMiddleware is added as the very innermost middleware, to deal with handled exception cases occurring in the routing or endpoints.
    exception_handlers - A mapping of either integer status codes, or exception class types onto callables which handle the exceptions. Exception handler callables should be of the form handler(request, exc) -> response and may be either standard functions, or async functions.
    on_startup - A list of callables to run on application startup. Startup handler callables do not take any arguments, and may be either standard functions, or async functions.
    on_shutdown - A list of callables to run on application shutdown. Shutdown handler callables do not take any arguments, and may be either standard functions, or async functions.
    lifespan - A lifespan context function, which can be used to perform startup and shutdown tasks. This is a newer style_path that replaces the on_startup and on_shutdown handlers. Use one or the other, not both.
    """
    def __init__(self, **kwargs):
        self.settings = spacestar_settings
        middleware = kwargs.pop('middleware', [])
        middleware.insert(0, session_middleware)
        self.module: str = kwargs.pop('module', 'main')
        self.app_name: str = kwargs.pop('app_name', 'app')
        self.lang: str = kwargs.pop('lang', 'en')
        self.title: str = kwargs.pop('title', 'SpaceStar')
        self.static_directory: Optional[str] = kwargs.pop('static_directory', None)
        self.templates_directory: Optional[str] = kwargs.pop('templates_directory', None)
        self.index_template: Optional[str] = kwargs.pop('index_template', tp.INDEX_TEMPLATE)
        self.head_template: Optional[str] = kwargs.pop('head_template', None)
        self.header_template: Optional[str] = kwargs.pop('header_template', None)
        self.footer_template: Optional[str] = kwargs.pop('footer_template', None)
        self.body_scripts: Optional[str] = kwargs.pop('body_scripts', None)

        if self.templates_directory:
            self.templates = Jinja2Templates(
                    directory=os.path.join(os.getcwd(), self.templates_directory),context_processors=[app_context])
        else:
            self.templates = Jinja2Templates(
                    env=jinja2.Environment(), context_processors=[app_context])

        super().__init__(middleware=middleware, **kwargs)
        if self.static_directory:
            self.routes.insert(1, Mount(
                    '/static',
                    app=StaticFiles(directory=os.path.join(os.getcwd(), self.static_directory)), name='static'))
    
    def set_global(self, name, value):
        self.templates.env.globals[name] = value
            
    @property
    def head(self) -> str:
        if self.head_template:
            if isinstance(self.head_template, str):
                return self.head_template
            return ''.join([str(i) for i in self.head_template])
        return ''
    
    @property
    def header(self) -> str:
        if self.header_template:
            if isinstance(self.header_template, str):
                return self.header_template
            return ''.join([str(i) for i in self.header_template])
        return tp.HEADER_TEMPLATE.format(self.title)
    
    @property
    def footer(self) -> str:
        if self.footer_template:
            if isinstance(self.footer_template, str):
                return self.footer_template
            return ''.join([str(i) for i in self.footer_template])
        return ''
        
    def from_string(self, source: str):
        return self.templates.env.from_string(source=source, globals=self.globals)
    
    @property
    def globals(self):
        return self.templates.env.globals
    
    @property
    def index_from_string(self):
        return self.from_string(self.index_template)
    
    async def home_page(self, request: Request, title: str | None = None):
        return self.response(request, title=title or self.title)

    @property
    def index(self) -> jinja2.Template:
        if self.templates_directory:
            return self.templates.get_template('index.html')
        return self.index_from_string
    
    @staticmethod
    def element(tag, *args, **kwargs):
        return cp.init_element(tag, *args, **kwargs)
    
    def render(self, request, / , template: str = None, source: str = None, **kwargs) -> str:
        kwargs['app'] = request.app
        kwargs['request'] = request
        if template:
            return self.templates.get_template(template).render(**kwargs)
        elif source:
            return self.from_string(source=source).render(**kwargs)
        return self.index.render(**kwargs)
    
    def response(self, request: Request, /, template: str = None, source: str = None, **kwargs) -> HTMLResponse:
        return HTMLResponse(self.render(request, template=template, source=source, **kwargs))
    
    def run(self, *args, **kwargs):
        if args:
            string = ':'.join(args)
        else:
            string = f'{self.module}:{self.app_name}'
        port = kwargs.pop('port', self.settings.port)
        uvicorn.run(string, port=port, **kwargs)
    
    def create_route(self, _endpoint=None, *, path: str = None, name: str = None, methods: list[str] = None):
        def decorator(endpoint):
            @wraps(endpoint)
            def wrapper():
                self.append(Route(path=path, endpoint=endpoint, name=name, methods=methods or ['GET']))
                return self
            return wrapper()
            
        if _endpoint is None:
            return decorator
        else:
            return decorator(_endpoint)
    
    def append(self, app: Route | Mount | Router) -> None:
        self.routes.append(app)
        
    def prepend(self, app: Route | Mount | Router) -> None:
        self.routes.insert(0, app)
        
    @property
    def E(self):
        return E

            



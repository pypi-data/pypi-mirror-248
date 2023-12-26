from __future__ import annotations

import io

from ormspace import model as md
from hx_markup import functions
from ormspace.keys import Key, TableKey
from starlette.requests import Request

from spacestar.component import init_element, Element


@md.modelmap
class SpaceModel(md.Model):
    
    @property
    def tablekey(self) -> str:
        return f'{self.table()}.{self.key}'
    
    @property
    def table_key(self) -> str:  #TODO: deletar
        return self.tablekey
    
    @classmethod
    def htmx(cls, **kwargs):
        return functions.join_htmx_attrs(**kwargs)
    
    @classmethod
    def field(cls, name: str):
        return cls.model_fields.get(name, None)
    
    async def display(self):
        with io.StringIO() as f:
            container: Element = init_element('div', id=self.table_key)
            container.children.append(init_element('h3', children=str(self)))
            container.children.append(init_element('ul', '.nav', children=[init_element('li','.nav-item', children=f'{k}: {v}') for k, v in dict(self).items()]))
            f.write(str(container))
            return f.getvalue()
        
    async def heading(self, tag: str, *args, **kwargs):
        with io.StringIO() as f:
            kwargs['children'] = str(self)
            f.write(str(init_element(tag, *args, **kwargs)))
            return f.getvalue()
        
    @classmethod
    def query_from_request(cls, request: Request):
        q, fields = {}, {**cls.model_fields}
        for k, v in request.query_params.items():
            q[f'{k}?contains'] = v.lower()
        return q
    
    @classmethod
    def query_from_dict(cls, data: dict):
        q, fields = {}, {**cls.model_fields}
        if data:
            for k, f in fields.items():
                if k in data.keys():
                    if f.annotation in [str, list[str]]:
                        q[f'{k}?contains'] = data[k]
        return q
        

        
    
    

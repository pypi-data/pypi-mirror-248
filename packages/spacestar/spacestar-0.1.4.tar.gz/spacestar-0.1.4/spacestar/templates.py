from __future__ import annotations

__ALL__ = ['BODY_SCRIPTS', 'HEAD_TEMPLATE', 'HEADER_TEMPLATE', 'FOOTER_TEMPLATE', 'INDEX_TEMPLATE', 'app_context']

import os
from typing import Any

from hx_markup import Element
from starlette.requests import Request

from spacestar import component as cp


def app_context(request: Request) -> dict[str, Any]:
    return {'app': request.app}

BODY_SCRIPTS = """
<script type="text/javascript">
function pixToFloat(string) {return Number.parseFloat(string.slice(0, -2))}
function pixToInt(string) {return Number.parseInt(string.slice(0, -2))}
function numberToPix(number) {return `${number}px`}
const getId = (id) => document.getElementById(id)

const body = getId('body');
const header = getId('header');
const main = getId('main');
const footer = getId('footer');

const circles = document.createElement('div');
circles.id = 'circles';
body.prepend(circles);
for(let i = 34; i-=1; i>=0){
    const circle = document.createElement('div');
    circle.className = 'circle';
    circle.id = `circle-${i}`;
    circle.style.display = 'block';
    circle.style.position = 'absolute';
    circle.style.bottom = `50%`;
    circle.style.left = `50%`;
    circle.style.zIndex = `100`;
    circle.style.transform = `scale(1)`;circle.style.opacity = `1`;
    circles.append(circle)
}
function getRandomInt(max) {return Math.floor(Math.random() * max);}
function getRandomFloat(max) {return Math.random() * max;}
function changeCircle(item){
    item.style.bottom = `${getRandomInt(50)}vh`;
    item.style.left = `${getRandomInt(100)}vw`;
    item.style.zIndex = `${-100 + getRandomInt(50)}`;
    item.style.transform = `scale(${getRandomInt(7)})`;
    item.style.opacity = `${getRandomFloat(.7)}`;
    }
function setupCircles(){circles.childNodes.forEach(item=>changeCircle(item))}
function setupPage(){
    const bodyHeight = getComputedStyle(body)['height'];
    const headerHeight = getComputedStyle(header)['height'];
    const footerHeight = getComputedStyle(footer)['height'];
    main.style.height = numberToPix(pixToFloat(bodyHeight) - pixToFloat(headerHeight) - pixToFloat(footerHeight));
        const wrapper = document.getElementById('wrapper');
    if(wrapper){
        wrapper.style.maxHeight = numberToPix(pixToFloat(main.style.height) - 30);
    }
    setupCircles();
}
body.onload = setupPage;
body.onresize = setupPage;
</script>"""

HEAD_TEMPLATE: str = """
<link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet"/>
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css");
:root{
    --primary-color: #f77903;
    --secondary-color: #777;
    --dark-color: #333;
    --light-color: #ddd;
    --body-background: radial-gradient(
        circle at 100%,
        var(--dark-color),
        var(--dark-color) 50%,
        var(--light-color) 75%,
        var(--dark-color) 75%
        );
    }
    * {padding: 0; margin: 0; box-sizing: border-box}
    html {overflow: hidden; height: 100vh; height: 100dvh}
    body {
        height: 100%;
        background-image: var(--body-background);
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
        > * {color: white}
    }
    legend, label, a {color: var(--primary-color);}
    #header{background-color: rgba(0, 0, 0, .5);}
    #main {display: grid; justify-content: center; align-items: center; align-content: center;}
    #wrapper {overflow-y: auto;}
    #footer{background-color: rgba(0, 0, 0, .5);}
    #circles{position: absolute; z-index: -100; top: 0; left: 0; width: 100%; height: 100%}
    .list-group-item {background-color: transparent}
    .darkorange {color: var(--primary-color);}
    .darkorange:hover {color: white; text-shadow: var(--primary-color) .125rem .125rem 1rem; transition: all 300ms;}
    .darkorange:focus{color: white; text-shadow: var(--primary-color) .125rem .125rem 1rem; border-block: var(--primary-color) solid .125rem; transition: all 300ms;}
    .small-caps{font-variant: small-caps;}
    .circle {width: 1vw; height: 1vw; bottom: 0; left: 50%; border-radius: 50%; background-image: radial-gradient(circle at 50%, var(--light-color), var(--primary-color)); transition: all 500ms ease-in-out; display: none;}

</style>
<script src="https://unpkg.com/htmx.org@1.9.10" integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC" crossorigin="anonymous"></script>
"""

HEADER_TEMPLATE = """
<header id="header" class="px-2">
    <h1><a href="/" class="text-white" style="text-decoration: none">{}</a></h1>
</header>
"""

FOOTER_TEMPLATE = """
        <footer id="footer" class="fixed-bottom px-2">
	        <div class="container-fluid" style="display: grid; grid-template-columns: 1fr 3fr 1fr">
				<div class=""></div>
				<div class="small-caps text-center">Sistema de Prontuário Eletrônico onde os dados são apenas seus.</div>
				<div class=""></div>
			</div>
        </footer>
	"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="utf-8"/>
        <meta content="width=device-width, initial-scale=1" name="viewport"/>
        <title>{{title or request.app.title}}</title>
        {{head or request.app.head}}
     </head>
     <body id="body">
        {{ header or request.app.header }}</header>
        <main id="main"><div id="wrapper" class="p-3 bg-dark bg-opacity-75">{{ main or request.app.main }}</div></main>
        {{ footer or request.app.footer }}
        {{ body_scripts or request.app.body_scripts }}
     </body>
</html>
"""


def create_templates_folder(path: str | os.PathLike = None, lang: str = None, title: str = None) -> None:
    templates_path = os.path.join(path or os.path.join(os.getcwd(), 'templates'))
    os.makedirs(templates_path, exist_ok=True)
    with open(f'{templates_path}/index.html', 'w') as f:
        f.write(str(cp.page_html(lang=lang or 'en', title=title or 'SpaceStar', children=[
                Element('h1', children=title or 'SpaceStar'),
                '{{content}}'
        ])))
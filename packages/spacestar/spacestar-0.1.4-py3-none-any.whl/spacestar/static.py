from __future__ import annotations

import os


def create_static_folder(path: str | os.PathLike = None) -> None:
    if not path:
        path = os.path.join(os.getcwd(), 'static')
    os.makedirs(path, exist_ok=True)
    os.makedirs(f'{path}/css', exist_ok=True)
    os.makedirs(f'{path}/js', exist_ok=True)

    with open(f'{path}/css/main.css', 'w') as f:
        f.write('* {margin: 0; padding: 0; box-sizing: border-box}\n')
    with open(f'{path}/js/main.js', 'w') as f:
        f.write('')
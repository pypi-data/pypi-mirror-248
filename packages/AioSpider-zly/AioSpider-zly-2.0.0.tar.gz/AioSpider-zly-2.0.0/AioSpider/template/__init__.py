from pathlib import Path

from AioSpider import tools
from AioSpider.tools.translate_tools import translate


def read_sts_tpl():
    path = Path(__file__).parent / 'settings.tpl'
    return path.read_text(encoding='utf-8')


def read_models_tpl():
    path = Path(__file__).parent / 'models.tpl'
    return path.read_text(encoding='utf-8')


def read_middleware_tpl():
    path = Path(__file__).parent / 'middleware.tpl'
    return path.read_text(encoding='utf-8')


def read_signals_tpl():
    path = Path(__file__).parent / f'signals.tpl'
    return path.read_text(encoding='utf-8')


def read_spider_tpl():
    path = Path(__file__).parent / f'spider.tpl'
    return path.read_text(encoding='utf-8')


def read_readme_tpl():
    path = Path(__file__).parent / f'README.tpl'
    return path.read_text(encoding='utf-8')


def gen_project(project: str, settings=True) -> list:

    path = Path.cwd() / project

    if path.exists():
        return None
    else:
        path.mkdir(parents=True, exist_ok=True)

    return [
        {'path': path / 'spiders', 'type': 'dir'},
        {'path': path / 'models', 'type': 'dir'},
        {'path': path / 'settings.py', 'type': 'file', 'text': read_sts_tpl() if settings else ''},
        {'path': path / 'models/models.py', 'type': 'file', 'text': read_models_tpl()},
        {'path': path / 'middleware.py', 'type': 'file', 'text': read_middleware_tpl()},
        {'path': path / 'signals.py', 'type': 'file', 'text': read_signals_tpl()},
        {'path': path / 'README.md', 'type': 'file', 'text': read_readme_tpl()},
    ]


def gen_spider(name, name_en=None, urls=None, source=None, target=None, help=None):

    text = read_spider_tpl()
    text = text.replace('{{ name }}', name)

    if name_en is None:
        text = text.replace('{{ name_en }}', 'Demo')
    else:
        text = text.replace('{{ name_en }}', name_en.title())

    if urls is None:
        text = text.replace('start_req_list = {{ start_req }}\n', '')
    else:
        s = '['
        for i in urls:
            s += f'\n{" " * 8}Request(\n{" " * 12}url="{i.strip()}"'

            if target is not None:
                s += f',\n{" " * 12}target="{target}"'

            if help is not None:
                s += f',\n{" " * 12}help="{help}"'

            s += f'\n{" " * 8}),'

        s += f'\n{" " * 4}]'
        
        text = text.replace('{{ start_req }}', s)
        
    if source is None:
        text = text.replace('{{ source }}', name)
    else:
        text = text.replace('{{ source }}', source)

    return text

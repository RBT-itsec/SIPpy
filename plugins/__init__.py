"""
Handle automatic plugin registration for this folder
via @register_plugin(<category>) decorator
"""

from importlib import import_module
from importlib import resources
from collections import defaultdict
from pathlib import Path

from typing import Callable, Dict, List

PLUGINS: Dict[str, Dict] = defaultdict(dict)


def register_plugin(category: str) -> Callable:
    """ Register function with category """
    def function_wrapper(func: Callable):
        """ Decorator to register functions """
        name: str = func.__name__
        PLUGINS[name]['func'] = func
        PLUGINS[name]['category'] = category
        return func
    return function_wrapper


def __getattr__(name: str) -> Callable:
    """ Return a named plugin """
    try:
        return PLUGINS[name]['func']
    except KeyError:
        _import_plugins()
        if name in PLUGINS:
            return PLUGINS[name]['func']
        else:
            raise AttributeError(
                f'module {__name__!r} has no attribute {name!r}'
            ) from None


def __dir__() -> List[str]:
    """ List available plugins """
    _import_plugins()
    return list(PLUGINS.keys())


def categories() -> List[str]:
    """ List available categories """
    return list({x['category'] for x in PLUGINS.values() if x.get('category')})

def get_category(name: str) -> str:
    """ Return the category of a given plugin name """
    return PLUGINS[name].get('category')

def _import_plugins() -> None:
    """ Import all resources to register plugins """
    for name in resources.contents(__name__):
        if name.endswith(".py"):
            path = Path(name)
            import_module(f"{__name__}.{path.stem}")

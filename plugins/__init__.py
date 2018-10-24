"""
Handle automatic plugin registration for this folder
via @register_plugin decorator
"""

from importlib import import_module
from importlib import resources
from collections import defaultdict
from pathlib import Path

from typing import Callable, Dict, List

PLUGINS = dict()


def register_plugin(func: Callable) -> Callable:
    """ Decorator to register functions """
    name: str = func.__name__
    PLUGINS[name] = func
    return func


def __getattr__(name: str) -> Callable:
    """ Return a named plugin """
    try:
        return PLUGINS[name]
    except KeyError:
        _import_plugins()
        if name in PLUGINS:
            return PLUGINS[name]
        else:
            raise AttributeError(
                f'module {__name__!r} has no attribute {name!r}'
            ) from None


def __dir__() -> List[str]:
    """ List available plugins """
    _import_plugins()
    return list(PLUGINS.keys())


def _import_plugins() -> None:
    """ Import all resources to register plugins """
    for name in resources.contents(__name__):
        if name.endswith(".py"):
            path = Path(name)
            import_module(f"{__name__}.{path.stem}")
            # import_module(f'{__name__}.{name[:-3]}')

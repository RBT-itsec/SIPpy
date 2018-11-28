"""
Handle automatic plugin registration for this folder
via @register_plugin(<category>) decorator
"""

from importlib import import_module
from importlib import resources
from collections import defaultdict
from pathlib import Path

from typing import Callable, Dict, List, Any

# PLUGINS: Dict[str, Dict[str, Any]] = defaultdict(dict)
PLUGINS = {}


class Plugin():  # TODO: Change to instance attributes instead
    # class attributes?!
    """ Generic Plugin """
    name: str = "plugin"
    category: str = "generic"

    def __init__(self):
        self.config = {}  # really needed?
        self.output = {}  # really needed?

    def run(self, target: str):
        """ Meta-method for running the plugin """
        return self._run(target)

    def _run(self, target: str):
        """ Run the plugin """
        print(f"{self.name} running: {self}")


def register_plugin(cls):
    name = cls.name
    if isinstance(cls, Plugin):
        PLUGINS[name] = cls
    else:
        PLUGINS[name] = cls()
    return cls


def __getattr__(name: str) -> Plugin:
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

# Copyright (c) 2019 ARGE Rundfunk-Betriebstechnik. MIT license, see LICENSE file.

"""
Handle automatic plugin registration for this folder
via @register_plugin or direct call of register_plugin
"""

from importlib import import_module
from importlib import resources
from collections import defaultdict
from pathlib import Path

from typing import Callable, Dict, List, Any, TypeVar, Type, Union


PLUGINS = {}


# Create Type PluginT for subclasses of Plugin without instance
PluginT = TypeVar('PluginT', bound='Plugin')


class Plugin():
    """ Generic Plugin """
    name: str = "plugin"
    category: str = "generic"

    def __init__(self):
        self.config: Dict = {}
        self.output: Dict = {}

    def run(self, target: str):
        """ Meta-method for running the plugin """
        return self._run(target)

    def _run(self, target: str):
        """ Run the plugin """
        print(f"{self.name} running: {target}")


# typing: Type[PluginT] for class/subclass, Plugin for instance/instance of subclass
def register_plugin(cls: Union[Type[PluginT], Plugin]):
    """ Register a class as plugin """
    name = cls.name
    # if we alreade have an instance, keep it
    # otherwise create one
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

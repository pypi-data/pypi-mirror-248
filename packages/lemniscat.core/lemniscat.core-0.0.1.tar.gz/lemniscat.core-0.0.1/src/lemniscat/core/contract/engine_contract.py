from logging import Logger
from typing import Optional, List

from lemniscat.core.model import Meta, TaskResult


class IPluginRegistry(type):
    plugin_registries: List[type] = list()

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if name != 'PluginCore':
            IPluginRegistry.plugin_registries.append(cls)


class PluginCore(object, metaclass=IPluginRegistry):
    """
    Plugin core class
    """

    meta: Optional[Meta]

    def __init__(self, logger: Logger) -> None:
        """
        Entry init block for plugins
        :param logger: logger that plugins can make use of
        """
        self._logger = logger
        
    def info(self) -> None:
        """
        Show plugin meta information
        :return: Meta
        """
        print('-----------------------------------------')
        print(f'Name: {self.meta.name}')
        print(f'Description: {self.meta.description}')
        print(f'Version: {self.meta.version}')
        print('-----------------------------------------')

    def invoke(self, **args) -> TaskResult:
        """
        Starts main plugin flow
        :param args: possible arguments for the plugin
        :return: a device for the plugin
        """
        pass
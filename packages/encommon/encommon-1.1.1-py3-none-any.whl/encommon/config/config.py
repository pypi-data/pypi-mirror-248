"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional

from .files import ConfigFiles
from .logger import Logger
from .paths import ConfigPaths
from ..types.dicts import merge_dicts
from ..utils.common import PATHABLE



class Config:
    """
    Contain the configurations from the arguments and files.

    :param files: Complete or relative path to config files.
    :param paths: Complete or relative path to config paths.
    :param cargs: Configuration arguments in dictionary form,
        which will override contents from the config files.
    """

    __files: ConfigFiles
    __paths: ConfigPaths
    __cargs: dict[str, Any]

    __config: Optional[dict[str, Any]]
    __merged: Optional[dict[str, Any]]
    __logger: Optional[Logger]


    def __init__(
        self,
        *,
        files: Optional[PATHABLE] = None,
        paths: Optional[PATHABLE] = None,
        cargs: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        files = files or []
        paths = paths or []
        cargs = cargs or {}

        self.__files = ConfigFiles(files)
        self.__cargs = deepcopy(cargs)
        self.__paths = ConfigPaths(paths)

        self.__config = None
        self.__merged = None
        self.__logger = None


    @property
    def files(
        self,
    ) -> ConfigFiles:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return self.__files


    @property
    def paths(
        self,
    ) -> ConfigPaths:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return self.__paths


    @property
    def cargs(
        self,
    ) -> dict[str, Any]:
        """
        Return the property for attribute from the class instance.

        :returns: Property for attribute from the class instance.
        """

        return self.__cargs


    @property
    def config(
        self,
    ) -> dict[str, Any]:
        """
        Return the configuration in dictionary format for files.

        :returns: Configuration in dictionary format for files.
        """

        if self.__config is not None:
            return deepcopy(self.__config)

        files = self.__files
        cargs = self.__cargs

        merged: dict[str, Any] = {}


        source = files.config

        for _, file in source.items():

            _source = file.config

            merge_dicts(
                dict1=merged,
                dict2=deepcopy(_source),
                force=False)


        merge_dicts(
            dict1=merged,
            dict2=deepcopy(cargs),
            force=True)


        self.__config = merged

        return deepcopy(self.__config)


    @property
    def merged(
        self,
    ) -> dict[str, Any]:
        """
        Return the configuration in dictionary format for paths.

        :returns: Configuration in dictionary format for paths.
        """

        if self.__merged is not None:
            return deepcopy(self.__merged)

        paths = self.__paths

        merged: dict[str, Any] = {}


        source = paths.config

        for _, path in source.items():

            _source = path.config

            for key, file in _source.items():
                merged[key] = file.config


        self.__merged = merged

        return deepcopy(self.__merged)


    @property
    def logger(
        self,
    ) -> Logger:
        """
        Initialize the Python logging library using parameters.
        """

        if self.__logger is not None:
            return self.__logger

        enlogger = self.config.get('enlogger', {})

        self.__logger = Logger(
            stdo_level=enlogger.get('stdo_level'),
            file_level=enlogger.get('file_level'),
            file_path=enlogger.get('file_path'))

        return self.__logger

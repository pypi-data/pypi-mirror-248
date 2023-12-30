"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import Any

from .common import config_load
from .common import config_path
from .common import config_paths
from ..utils.common import PATHABLE



class ConfigFile:
    """
    Contain the configuration content from filesystem path.

    :param path: Complete or relative path to configuration.
    """

    path: Path
    config: dict[str, Any]


    def __init__(
        self,
        path: str | Path,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.path = config_path(path)
        self.config = config_load(path)



class ConfigFiles:
    """
    Enumerate files and store the contents on relative path.

    .. note::
       Class can be empty in order to play nice with parent.

    :param paths: Complete or relative path to config files.
    :param force: Force the merge on earlier files by later.
    """

    paths: tuple[Path, ...]
    config: dict[str, ConfigFile]


    def __init__(
        self,
        paths: PATHABLE,
        force: bool = False,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.paths = config_paths(paths)

        self.config = {
            str(x): ConfigFile(x)
            for x in self.paths}

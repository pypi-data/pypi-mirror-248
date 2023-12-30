"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from glob import glob
from pathlib import Path

from .common import config_path
from .common import config_paths
from .files import ConfigFile
from ..utils.common import PATHABLE



class ConfigPath:
    """
    Contain the configuration content from filesystem path.

    :param path: Complete or relative path to configuration.
    """

    path: Path
    config: dict[str, ConfigFile]


    def __init__(
        self,
        path: str | Path,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.path = config_path(path)

        glob_path = [
            f'{self.path}/*.yml',
            f'{self.path}/**/*.yml']

        self.config = {
            str(y): ConfigFile(y)
            for x in glob_path
            for y in glob(x, recursive=True)}



class ConfigPaths:
    """
    Enumerate paths and store the contents on relative path.

    .. note::
       Class can be empty in order to play nice with parent.

    :param paths: Complete or relative path to config paths.
    :param force: Force the merge on earlier files by later.
    """

    paths: tuple[Path, ...]
    config: dict[str, ConfigPath]


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
            str(x): ConfigPath(x)
            for x in self.paths}

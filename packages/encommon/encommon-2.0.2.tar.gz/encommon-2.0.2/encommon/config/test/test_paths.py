"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from ..paths import ConfigPath
from ..paths import ConfigPaths



def test_ConfigPath(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    path = ConfigPath(config_path)

    assert len(path.__dict__) == 2

    assert hasattr(path, 'path')
    assert hasattr(path, 'config')

    assert path.path == config_path
    assert len(path.config) == 4



def test_ConfigPaths(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    paths = ConfigPaths(config_path)

    assert len(paths.__dict__) == 2
    assert len(paths.config) == 1


    assert len(paths.paths) == 1
    assert len(paths.config) == 1


    assert hasattr(paths, 'paths')
    assert hasattr(paths, 'config')

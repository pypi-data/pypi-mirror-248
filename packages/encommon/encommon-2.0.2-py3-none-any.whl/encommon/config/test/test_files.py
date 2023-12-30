"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from ..files import ConfigFile
from ..files import ConfigFiles



def test_ConfigFile(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    file = ConfigFile(
        f'{config_path}/one/one.yml')

    assert len(file.__dict__) == 2

    assert hasattr(file, 'path')
    assert hasattr(file, 'config')

    assert file.path.name == 'one.yml'
    assert file.config == {'foo': 'bar'}



def test_ConfigFiles(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    files = ConfigFiles([
        f'{config_path}/one/one.yml',
        f'{config_path}/one/two.yml'])

    assert len(files.__dict__) == 2

    assert hasattr(files, 'paths')
    assert hasattr(files, 'config')


    assert len(files.paths) == 2
    assert len(files.config) == 2


    files = ConfigFiles(
        f'{config_path}/one/one.yml')

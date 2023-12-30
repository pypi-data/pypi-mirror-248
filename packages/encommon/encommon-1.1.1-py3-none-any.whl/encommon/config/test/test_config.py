"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from ..config import Config
from ..logger import Logger
from ... import ENPYRWS
from ...utils.sample import load_sample
from ...utils.sample import prep_sample



SAMPLES = (
    Path(__file__).parent
    .joinpath('samples'))



def test_Config(  # noqa: CFQ001
    config_path: Path,
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    :param tmp_path: pytest object for temporal filesystem.
    """

    (config_path
        .joinpath('one.yml')
        .write_text(
            'stdo_level: info\n'))

    (config_path
        .joinpath('two.yml')
        .write_text(
            'stdo_level: debug\n'
            'file_level: info\n'))


    config = Config(
        files=[
            f'{config_path}/one.yml',
            f'{config_path}/two.yml'],
        paths=[config_path, tmp_path],
        cargs={'file_level': 'warning'})

    assert len(config.__dict__) == 6

    assert hasattr(config, '_Config__files')
    assert hasattr(config, '_Config__paths')
    assert hasattr(config, '_Config__cargs')
    assert hasattr(config, '_Config__config')
    assert hasattr(config, '_Config__merged')


    assert list(config.files.paths) == [
        Path(f'{config_path}/one.yml'),
        Path(f'{config_path}/two.yml')]

    assert list(config.paths.paths) == [
        Path(f'{config_path}')]

    assert config.cargs == {
        'file_level': 'warning'}


    assert len(config.config) == 2

    _config1 = config.config
    _config2 = config.config

    assert _config1 is not _config2

    sample = load_sample(
        path=SAMPLES.joinpath('config.json'),
        update=ENPYRWS,
        content=_config1,
        replace={
            'config_path': str(config_path),
            'tmp_path': str(tmp_path)})

    expect = prep_sample(
        content=_config2,
        replace={
            'config_path': str(config_path),
            'tmp_path': str(tmp_path)})

    assert sample == expect


    assert sorted(config.merged) == [
        f'{config_path}/one.yml',
        f'{config_path}/one/one.yml',
        f'{config_path}/one/two.yml',
        f'{config_path}/two.yml',
        f'{config_path}/two/one.yml',
        f'{config_path}/two/two.yml']

    _merged1 = config.merged
    _merged2 = config.merged

    assert _merged1 is not _merged2

    sample = load_sample(
        path=SAMPLES.joinpath('merged.json'),
        update=ENPYRWS,
        content=_merged1,
        replace={
            'config_path': str(config_path),
            'tmp_path': str(tmp_path)})

    expect = prep_sample(
        content=_merged2,
        replace={
            'config_path': str(config_path),
            'tmp_path': str(tmp_path)})

    assert sample == expect


    logger = config.logger

    assert isinstance(logger, Logger)

    _logger1 = config.logger
    _logger2 = config.logger

    assert _logger1 is _logger2

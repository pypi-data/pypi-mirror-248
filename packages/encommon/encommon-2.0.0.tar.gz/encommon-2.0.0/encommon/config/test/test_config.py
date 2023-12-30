"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from ..config import Config
from ..logger import Logger
from ... import ENPYRWS
from ...crypts.crypts import Crypts
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
            'enconfig:\n'
            f'  paths: ["{config_path}"]\n'
            'enlogger:\n'
            '  stdo_level: info\n'))

    (config_path
        .joinpath('two.yml')
        .write_text(
            'encrypts:\n'
            '  phrases:\n'
            '    default: fernetpassphrase\n'
            'enlogger:\n'
            '  stdo_level: debug\n'
            '  file_level: info\n'))


    config = Config(
        files=[
            f'{config_path}/one.yml',
            f'{config_path}/two.yml'],
        cargs={
            'enlogger': {
                'file_level': 'warning'}})

    assert len(config.__dict__) == 8

    assert hasattr(config, '_Config__files')
    assert hasattr(config, '_Config__paths')
    assert hasattr(config, '_Config__cargs')
    assert hasattr(config, '_Config__model')
    assert hasattr(config, '_Config__config')
    assert hasattr(config, '_Config__merged')
    assert hasattr(config, '_Config__logger')
    assert hasattr(config, '_Config__crypts')


    assert list(config.files.paths) == [
        Path(f'{config_path}/one.yml'),
        Path(f'{config_path}/two.yml')]

    assert list(config.paths.paths) == [
        Path(f'{config_path}')]

    assert config.cargs == {
        'enlogger': {
            'file_level': 'warning'}}

    assert hasattr(config.model, 'model_dump')


    assert len(config.config) == 3

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


    crypts = config.crypts

    assert isinstance(crypts, Crypts)

    _crypts1 = config.crypts
    _crypts2 = config.crypts

    assert _crypts1 is _crypts2

"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from pytest import fixture



@fixture
def config_path(
    tmp_path: Path,
) -> Path:
    """
    Construct the directory and files needed for the tests.

    :param tmp_path: pytest object for temporal filesystem.
    """

    for name in ['one', 'two']:

        parent = Path(f'{tmp_path}/{name}')

        Path.mkdir(parent)

        (parent
            .joinpath('one.yml')
            .write_text('foo: bar'))

        (parent
            .joinpath('two.yml')
            .write_text('foo: bar'))

    return tmp_path

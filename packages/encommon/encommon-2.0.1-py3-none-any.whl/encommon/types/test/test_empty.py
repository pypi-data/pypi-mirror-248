"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import copy
from copy import deepcopy

from ..empty import Empty
from ..empty import EmptyType



def test_EmptyType() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    empty = EmptyType()

    assert len(empty.__dict__) == 1

    assert hasattr(empty, '_EmptyType__empty')


    assert repr(EmptyType()) == 'EmptyType'
    assert repr(EmptyType)[8:-2] == (
        'encommon.types.empty.EmptyType')

    assert isinstance(hash(EmptyType()), int)

    assert str(EmptyType()) == 'EmptyType'
    assert str(EmptyType)[8:-2] == (
        'encommon.types.empty.EmptyType')


    assert not (Empty or None)
    assert Empty is Empty
    assert Empty is EmptyType()
    assert Empty == Empty
    assert Empty == EmptyType()
    assert Empty is not None
    assert Empty != 'Empty'

    assert deepcopy(Empty) is Empty
    assert copy(Empty) is Empty

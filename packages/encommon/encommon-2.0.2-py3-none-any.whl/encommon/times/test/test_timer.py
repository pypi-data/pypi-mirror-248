"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep

from pytest import raises

from ..timer import Timer



def test_Timer() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    timer = Timer({'one': 1})

    assert len(timer.__dict__) == 2

    assert hasattr(timer, '_Timer__timer')
    assert hasattr(timer, '_Timer__cache')


    assert repr(timer).startswith(
        '<encommon.times.timer.Timer')

    assert str(timer).startswith(
        '<encommon.times.timer.Timer')


    assert timer.mapping == {'one': 1}

    assert not timer.ready('one')
    sleep(1.1)
    assert timer.ready('one')


    timer.create('two', 2, 0)

    assert timer.ready('two')
    assert not timer.ready('two')



def test_Timer_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    timer = Timer({'one': 1})


    with raises(ValueError) as reason:
        timer.ready('dne')

    assert str(reason.value) == 'unique'


    with raises(ValueError) as reason:
        timer.update('dne')

    assert str(reason.value) == 'unique'


    with raises(ValueError) as reason:
        timer.create('one', 1)

    assert str(reason.value) == 'unique'

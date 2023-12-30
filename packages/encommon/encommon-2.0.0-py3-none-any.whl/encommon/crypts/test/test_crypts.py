"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pytest import mark
from pytest import raises

from ..crypts import Crypts



_PHRASES = {
    'default': Crypts.keygen(),
    'secrets': Crypts.keygen()}



def test_Crypts() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    crypts = Crypts(_PHRASES)

    assert len(crypts.__dict__) == 1

    assert hasattr(crypts, '_Crypts__phrases')


    assert repr(crypts).startswith(
        '<encommon.crypts.crypts.Crypts')

    assert str(crypts).startswith(
        '<encommon.crypts.crypts.Crypts')


    assert crypts.phrases == _PHRASES



@mark.parametrize(
    'value,unique',
    [('foo', 'default'),
     ('foo', 'secrets')])
def test_Crypts_iterate(
    value: str,
    unique: str,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param value: String value that will returned encrypted.
    :param unique: Unique identifier of mapping passphrase.
    """

    crypts = Crypts(_PHRASES)

    encrypt = crypts.encrypt(value, unique)

    split = encrypt.split(';')

    assert split[1] == '1.0'
    assert split[2] == unique

    decrypt = crypts.decrypt(encrypt)

    assert decrypt == value



def test_Crypts_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    with raises(ValueError) as reason:
        Crypts({'foo': 'bar'})

    assert str(reason.value) == 'default'


    crypts = Crypts(_PHRASES)


    with raises(ValueError) as reason:
        crypts.decrypt('foo')

    assert str(reason.value) == 'string'


    with raises(ValueError) as reason:
        crypts.decrypt('$ENCRYPT;1.1;f;oo')

    assert str(reason.value) == 'version'

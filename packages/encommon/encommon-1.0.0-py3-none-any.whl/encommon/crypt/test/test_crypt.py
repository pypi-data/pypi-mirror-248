"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pytest import mark
from pytest import raises

from ..crypt import Crypt



_PHRASES = {
    'default': Crypt.keygen(),
    'secrets': Crypt.keygen()}



def test_Crypt() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    crypt = Crypt(_PHRASES)

    assert len(crypt.__dict__) == 1

    assert hasattr(crypt, '_Crypt__phrase')


    assert repr(crypt).startswith(
        '<encommon.crypt.crypt.Crypt')

    assert str(crypt).startswith(
        '<encommon.crypt.crypt.Crypt')


    assert crypt.mapping == _PHRASES



@mark.parametrize(
    'value,unique',
    [('foo', 'default'),
     ('foo', 'secrets')])
def test_Crypt_iterate(
    value: str,
    unique: str,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param value: String value that will returned encrypted.
    :param unique: Unique identifier of mapping passphrase.
    """

    crypt = Crypt(_PHRASES)

    encrypt = crypt.encrypt(value, unique)

    split = encrypt.split(';')

    assert split[1] == '1.0'
    assert split[2] == unique

    decrypt = crypt.decrypt(encrypt)

    assert decrypt == value



def test_Crypt_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    with raises(ValueError) as reason:
        Crypt({'foo': 'bar'})

    assert str(reason.value) == 'default'


    crypt = Crypt(_PHRASES)


    with raises(ValueError) as reason:
        crypt.decrypt('foo')

    assert str(reason.value) == 'string'


    with raises(ValueError) as reason:
        crypt.decrypt('$ENCRYPT;1.1;f;oo')

    assert str(reason.value) == 'version'

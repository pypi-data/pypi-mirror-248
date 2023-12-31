import datetime
import decimal
import math
import re
from decimal import Decimal
from typing import cast, Pattern, Type, TypeVar

delta_type = datetime.timedelta | int | float
Number = int | float
DecimalNumber = Number | Decimal
_TN = TypeVar('_TN', bound=DecimalNumber)

ExceptionType = Type[Exception]
ExceptionsType = tuple[ExceptionType, ...] | ExceptionType
StringTypes = str | bytes


def timedelta_to_seconds(delta: datetime.timedelta) -> Number:
    '''Convert a timedelta to seconds with the microseconds as fraction

    Note that this method has become largely obsolete with the
    `timedelta.total_seconds()` method introduced in Python 2.7.

    >>> from datetime import timedelta
    >>> '%d' % timedelta_to_seconds(timedelta(days=1))
    '86400'
    >>> '%d' % timedelta_to_seconds(timedelta(seconds=1))
    '1'
    >>> '%.6f' % timedelta_to_seconds(timedelta(seconds=1, microseconds=1))
    '1.000001'
    >>> '%.6f' % timedelta_to_seconds(timedelta(microseconds=1))
    '0.000001'
    '''
    # Only convert to float if needed
    if delta.microseconds:
        total = delta.microseconds * 1e-6
    else:
        total = 0
    total += delta.seconds
    total += delta.days * 60 * 60 * 24
    return total


def delta_to_seconds(interval: delta_type) -> float:
    '''
    Convert a timedelta to seconds

    >>> delta_to_seconds(datetime.timedelta(seconds=1))
    1
    >>> delta_to_seconds(datetime.timedelta(seconds=1, microseconds=1))
    1.000001
    >>> delta_to_seconds(1)
    1
    >>> delta_to_seconds('whatever')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Unknown type ...
    '''
    if isinstance(interval, datetime.timedelta):
        return timedelta_to_seconds(interval)
    if isinstance(interval, (int, float)):
        return interval
    raise TypeError('Unknown type %s: %r' % (type(interval), interval))


def to_int(
    input_: str | None = None,
    default: int = 0,
    exception: ExceptionsType = (ValueError, TypeError),
    regexp: Pattern[str] | None = None,
) -> int:
    r'''
    Convert the given input to an integer or return default

    When trying to convert the exceptions given in the exception parameter
    are automatically catched and the default will be returned.

    The regexp parameter allows for a regular expression to find the digits
    in a string.
    When True it will automatically match any digit in the string.
    When a (regexp) object (has a search method) is given, that will be used.
    WHen a string is given, re.compile will be run over it first

    The last group of the regexp will be used as value

    >>> to_int('abc')
    0
    >>> to_int('1')
    1
    >>> to_int('')
    0
    >>> to_int()
    0
    >>> to_int('abc123')
    0
    >>> to_int('123abc')
    0
    >>> to_int('abc123', regexp=True)
    123
    >>> to_int('123abc', regexp=True)
    123
    >>> to_int('abc123abc', regexp=True)
    123
    >>> to_int('abc123abc456', regexp=True)
    123
    >>> to_int('abc123', regexp=re.compile(r'(\d+)'))
    123
    >>> to_int('123abc', regexp=re.compile(r'(\d+)'))
    123
    >>> to_int('abc123abc', regexp=re.compile(r'(\d+)'))
    123
    >>> to_int('abc123abc456', regexp=re.compile(r'(\d+)'))
    123
    >>> to_int('abc123', regexp=r'(\d+)')
    123
    >>> to_int('123abc', regexp=r'(\d+)')
    123
    >>> to_int('abc', regexp=r'(\d+)')
    0
    >>> to_int('abc123abc', regexp=r'(\d+)')
    123
    >>> to_int('abc123abc456', regexp=r'(\d+)')
    123
    >>> to_int('1234', default=1)
    1234
    >>> to_int('abc', default=1)
    1
    >>> to_int('abc', regexp=123)
    Traceback (most recent call last):
    ...
    TypeError: unknown argument for regexp parameter: 123
    '''
    if regexp is True:
        regexp = re.compile(r'(\d+)')
    elif isinstance(regexp, str):
        regexp = re.compile(regexp)
    elif hasattr(regexp, 'search'):
        pass
    elif regexp is not None:
        raise TypeError('unknown argument for regexp parameter: %r' % regexp)

    try:
        if regexp and input_:
            if match := regexp.search(input_):
                input_ = match.groups()[-1]

        if input_ is None:
            return default
        return int(input_)
    except exception:  # type: ignore
        return default


def to_unicode(
    input_: StringTypes,
    encoding: str = 'utf-8',
    errors: str = 'replace',
) -> str:
    '''Convert objects to unicode, if needed decodes string with the given
    encoding and errors settings.

    :rtype: str

    >>> to_unicode(b'a')
    'a'
    >>> to_unicode('a')
    'a'
    >>> to_unicode(u'a')
    'a'
    >>> class Foo(object): __str__ = lambda s: u'a'
    >>> to_unicode(Foo())
    'a'
    >>> to_unicode(Foo)
    "<class 'progressbar.converters.Foo'>"
    '''
    if isinstance(input_, bytes):
        return input_.decode(encoding, errors)
    return str(input_)


def scale_1024(
    x: Number,
    n_prefixes: int,
) -> tuple[Number, Number]:
    '''Scale a number down to a suitable size, based on powers of 1024.

    Returns the scaled number and the power of 1024 used.

    Use to format numbers of bytes to KiB, MiB, etc.

    >>> scale_1024(310, 3)
    (310.0, 0)
    >>> scale_1024(2048, 3)
    (2.0, 1)
    >>> scale_1024(0, 2)
    (0.0, 0)
    >>> scale_1024(0.5, 2)
    (0.5, 0)
    >>> scale_1024(1, 2)
    (1.0, 0)
    '''
    if x <= 0:
        power = 0
    else:
        power = min(int(math.log(x, 2) / 10), n_prefixes - 1)
    scaled = float(x) / (2 ** (10 * power))
    return scaled, power


def remap(
    value: _TN,
    old_min: _TN,
    old_max: _TN,
    new_min: _TN,
    new_max: _TN,
) -> _TN:
    '''
    remap a value from one range into another.

    >>> remap(500, 0, 1000, 0, 100)
    50
    >>> remap(250.0, 0.0, 1000.0, 0.0, 100.0)
    25.0
    >>> remap(-75, -100, 0, -1000, 0)
    -750
    >>> remap(33, 0, 100, -500, 500)
    -170
    >>> remap(decimal.Decimal('250.0'), 0.0, 1000.0, 0.0, 100.0)
    Decimal('25.0')

    This is a great use case example. Take an AVR that has dB values the
    minimum being -80dB and the maximum being 10dB and you want to convert
    volume percent to the equilivint in that dB range

    >>> remap(46.0, 0.0, 100.0, -80.0, 10.0)
    -38.6

    I added using decimal.Decimal so floating point math errors can be avoided.
    Here is an example of a floating point math error
    >>> 0.1 + 0.1 + 0.1
    0.30000000000000004

    If floating point remaps need to be done my suggstion is to pass at least
    one parameter as a `decimal.Decimal`. This will ensure that the output
    from this function is accurate. I left passing `floats` for backwards
    compatability and there is no conversion done from float to
    `decimal.Decimal` unless one of the passed parameters has a type of
    `decimal.Decimal`. This will ensure that any existing code that uses this
    funtion will work exactly how it has in the past.

    Some edge cases to test
    >>> remap(1, 0, 0, 1, 2)
    Traceback (most recent call last):
    ...
    ValueError: Input range (0-0) is empty

    >>> remap(1, 1, 2, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Output range (0-0) is empty

    :param value: value to be converted
    :type value: int, float, decimal.Decimal

    :param old_min: minimum of the range for the value that has been passed
    :type old_min: int, float, decimal.Decimal

    :param old_max: maximum of the range for the value that has been passed
    :type old_max: int, float, decimal.Decimal

    :param new_min: the minimum of the new range
    :type new_min: int, float, decimal.Decimal

    :param new_max: the maximum of the new range
    :type new_max: int, float, decimal.Decimal

    :return: value that has been re ranged. if any of the parameters passed is
        a `decimal.Decimal` all of the parameters will be converted to
        `decimal.Decimal`.  The same thing also happens if one of the
        parameters is a `float`. otherwise all parameters will get converted
        into an `int`. technically you can pass a `str` of an integer and it
        will get converted. The returned value type will be `decimal.Decimal`
        of any of the passed parameters ar `decimal.Decimal`, the return type
        will be `float` if any of the passed parameters are a `float` otherwise
        the returned type will be `int`.

    :rtype: int, float, decimal.Decimal
    '''
    type_: Type[DecimalNumber]
    if (
        isinstance(value, decimal.Decimal)
        or isinstance(old_min, decimal.Decimal)
        or isinstance(old_max, decimal.Decimal)
        or isinstance(new_min, decimal.Decimal)
        or isinstance(new_max, decimal.Decimal)
    ):
        type_ = decimal.Decimal
    elif (
        isinstance(value, float)
        or isinstance(old_min, float)
        or isinstance(old_max, float)
        or isinstance(new_min, float)
        or isinstance(new_max, float)
    ):
        type_ = float

    else:
        type_ = int

    value = cast(_TN, type_(value))
    old_min = cast(_TN, type_(old_min))
    old_max = cast(_TN, type_(old_max))
    new_max = cast(_TN, type_(new_max))
    new_min = cast(_TN, type_(new_min))

    # These might not be floats but the Python type system doesn't understand
    # the generic type system in this case
    old_range = cast(float, old_max) - cast(float, old_min)
    new_range = cast(float, new_max) - cast(float, new_min)

    if old_range == 0:
        raise ValueError(f'Input range ({old_min}-{old_max}) is empty')

    if new_range == 0:
        raise ValueError(f'Output range ({new_min}-{new_max}) is empty')

    new_value = (value - old_min) * new_range  # type: ignore

    if type_ == int:
        new_value //= old_range  # type: ignore
    else:
        new_value /= old_range  # type: ignore

    new_value += new_min  # type: ignore

    return cast(_TN, new_value)

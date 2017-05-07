"""Library of input functions with type conversion

Builtin function 'input' does not support scan formatted. Also,
its return value can only be string. Users should do extra
parsing actions and type conversions to get what they want.

This module provides several wrappers of builtin 'input'.
They can statisfy above requirements easily.

Available functions:
	finput: Read input by format string.
	tinput: Read input and split them into several values with
			specified type.
"""

import re
from ast import literal_eval
from functools import partial


class Error(Exception):
	"""Base class for all exceptions raised by this module"""
	pass

class InputDoesNotMatchFStr(Error):
	"""Raised if input does not match format string"""
	pass

class TypeConvertError(Error):
	"""Raised if input can not be converted to specified type"""
	pass

class InputCountNotInRange(Error):
	"""Raised if input count is not in the specified range"""
	pass


# followings are default format placeholders
_FORMAT_PLACEHOLDER = {
    '%a': literal_eval,
    '%d': int,
    '%f': float,
    '%o': partial(int, base=8),
    '%s': str,
    '%x': partial(int, base=16),
}


def finput(prompt='', fstr='%s', expand_fph=None, whitespace=False,
		   escape_parenthesis=True):
    """Read input by format string
    
    This function is a wrapper of builtin function 'input'.
    User can specify self-defined format string 'fstr' to scan formatted.
    It is just like 'scanf' in programming language C.

    Args:
		prompt: A prompt string.
		fstr: Format string contains format placeholders to capture wanted
			value. It also supports regular expressions.
		expand_fph: A dictionary which is used to expand the default format
		    placeholders. The key of expand_fph is a format specifier(string)
		    which starts with character '%' with length 2.
		whitespace: A boolean indicates whether the placeholder captures
			unicode whitespace.
		escape_parenthesis: A boolean indicate the parenthesis occurs in fstr
			should be escaped.

    Returns:
        A tuple of captured values.

    Default Format Placeholders:
    	%a: Capture any string which represents a legal Python object.
			Use 'ast.literal_eval' to convert captured string.
		%d: Capture string represents a decimal integer.
			Use 'int' with base '10' to convert captured string.
		%f: Capture string represents a floating.
			Use 'float' to convert captured string.
		%o: Capture string represents an octal integer.
			Use 'int' with base '8' to convert captured string.
		%s: Capture string represents a Python string.
			Use 'str' to convert captured string
		%h: Capture string represents a hexadecimal integer.
			Use 'int' with base '16' to convert captured string.
    """
    fph = _FORMAT_PLACEHOLDER
    if expand_fph is not None:
        fph.update(expand_fph)
    if escape_parenthesis:
        rstr = fstr.replace('(', '\(').replace(')', '\)')
    else:
        rstr = fstr
    regex = '(.+)' if whitespace else '(\S+)'
    for sp, typ in fph.items():
        rstr = rstr.replace(sp, regex)
    types = []
    for idx, c in enumerate(fstr):
        pattern = fstr[idx:idx+2]
        if pattern in fph:
            types.append(fph[pattern])
    pure_input = input(prompt)
    mobj = re.match(rstr, pure_input)
    if mobj:
        try:
            return tuple(typ(value) for value, typ in zip(mobj.groups(), types))
        except Exception as err:
            raise TypeConvertError(err)
    else:
        msg = 'input does not match format string "{}"'
        raise InputDoesNotMatchFStr(msg.format(fstr))


def tinput(prompt='', typ=str, sep=None, min=1, max=100000):
    """Read input and split them into several values with specified type

    This function is a wrapper of builtin function 'input'.
    User can read several values with specified type from input.

    Args:
    	prompt: A prompt string.
    	typ: A function or callable object which can convert the string to
    		wanted type.
    	sep: A string which is used to split the original input string.
    		If sep is None, this function splits string by arbitrary blanks
    		just like builtin function 'split' with no arguments.
    	min: An integer indicates the minimum of values. If the input count
    		is less than this value, raise 'InputCountNotInRange'.
    	max: An integer indicates the maximum of values. If the input count
    		is greater than this value, raise 'InputCountNotInRange'.

    Returns:
    	A tuple of captured values with specified type.
    """
    pure_input = input(prompt)
    try:
        if sep is None:
            values = tuple(typ(item) for item in pure_input.split())
        else:
            values = tuple(typ(item) for item in pure_input.split(sep))
    except Exception as err:
        raise TypeConvertError(err)
    if len(values) < min or len(values) > max:
        msg = 'input count {} is not in range [{}, {}]'
        raise InputCountNotInRange(msg.format(len(values), min, max))
    return values
tinp
=====

Builtin function ``input`` does not support scan formatted. Also, its return value can only be string. Users should do extra parsing actions and type conversions to get what they want.

This module provides several wrappers of builtin ``input``. They can statisfy above requirements easily.

## Installation

```bash
$ pip install tinp
```

or you can clone this repo directly.

```bash
$ git clone https://github.com/dokelung/tinp.git
```

## Examples

### finput

Read input by format string:

```python
>>> from tinp import finput
>>> finput(prompt='==> ', fstr='%d, %f, %s')
==> 88, 12.3, hello
(88, 12.3, 'hello')
```

### tinput

Read input and split it into several values with specified type:

```python
>>> from tinp import tinput
>>> tinput(prompt='please enter 5 integers: ', typ=int)
please enter 5 integers: 1 2 3 4 5
(1, 2, 3, 4, 5)
```

### einput

Read input and evaluate it:

```python
>>> from tinp import einput
>>> einput(prompt='==> ', typ=float)
==> 2+2
4.0
```

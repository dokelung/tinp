tinp
=====

Builtin function ``input`` does not support scan formatted. Also, its return value can only be string. Users should do extra parsing actions and type conversions to get what they want.

This module provides several wrappers of builtin ``input``. They can statisfy above requirements easily.

## Example

### finput

```python
>>> from tinp import finput
>>> finput(prompt='==> ', fstr='%d, %f, %s')
==> 88, 12.3, hello
(88, 12.3, 'hello')
```

### tinput

```python
>>> from tinp import tinput
>>> tinput(prompt='please enter 5 integers: ', typ=int)
please enter 5 integers: 1 2 3 4 5
(1, 2, 3, 4, 5)
```

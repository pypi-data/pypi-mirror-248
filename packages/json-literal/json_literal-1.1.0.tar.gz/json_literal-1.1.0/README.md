# Use JSON literal on Python code

By importing this package in wildcard, JSON data can be handled directly in Python code.

# Install

```sh
pip install json-literal
```

# Usage

```python
from json_literal import *

data = {
    "a": 1,
    "b": true,
    "c": false,
    "d": null,
    "e": [1,2,3],
    "f": {
        "g": "h"
    }
}
```

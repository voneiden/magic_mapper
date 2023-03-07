# Magicmapper

Unconventional (?) approach to mapping data from one object to another. 


# Usage
Check out test_magic.py for some examples. The fundamental idea is that we 
define a target schema which we can populate using the magicmapper. 
Consider the following source data

```python 
source_data = [
    {
        "person": {
            "name": "foo1"
        }
    },
    {
        "person": {
            "name": "foo2"
        }
    },
]
```

Say we'd like to map this to this


```python 
destination_data = [
    {
        "name": "foo1"
    },
    {
        "name": "foo2"
    },
]
```

This could be done with the following magicmapping

```python
from magicmapper import magic_map, Schema, Value


magic_map([Schema({"name": Value("person") >> Value("name")})], test_source_data)
```
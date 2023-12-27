# polyants
> POLYHUB system helpers.

[![pipeline status](https://gitlab.com/ru-r5/polyants/badges/master/pipeline.svg)](https://gitlab.com/ru-r5/polyants/-/commits/master)
[![PyPI version](https://badge.fury.io/py/polyants.png)](https://badge.fury.io/py/polyants)

![](polyants.png)

## Installation

OS X & Linux & Windows:

```sh
pip install polyants
```

## Usage example

```python
from polyants.adapters import dict_to_enumdef

SomeEnum = dict_to_enumdef('SomeEnum', {'A': 'a'})
print(SomeEnum.A.value)
```

## Development setup
- coverage

```sh
$ poetry run pytest --cov
```

- format

```sh
$ poetry run black polyants -S
```

- lint

```sh
$ poetry run flakehell lint
```

- type checking

```sh
$ poetry run pyre
```

## Release History
- 0.2a0
  - configurable enum class (#3)
- 0.1a0
  - mvp (#1)

## Meta

pymancer@gmail.com ([Polyanalitika LLC](https://polyanalitika.ru))  
[https://gitlab.com/ru-r5/polyants](https://gitlab.com/ru-r5/polyants)

## License

This Source Code Form is subject to the terms of the Mozilla Public  
License, v. 2.0. If a copy of the MPL was not distributed with this  
file, You can obtain one at https://mozilla.org/MPL/2.0/.  

## Contributing

1. Fork it (<https://gitlab.com/ru-r5/polyants/fork>)
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -am 'Add some foo'`)
4. Push to the branch (`git push origin feature/foo`)
5. Create a new Pull Request

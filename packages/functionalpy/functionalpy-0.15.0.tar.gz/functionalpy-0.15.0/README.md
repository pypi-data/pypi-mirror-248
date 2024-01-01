# FunctionalPy
[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)][dev container]
[![PyPI](https://img.shields.io/pypi/v/functionalpy.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/FunctionalPy)][pypi status]
[![Tests](https://github.com/MartinBernstorff/FunctionalPy/actions/workflows/tests.yml/badge.svg)][tests]

[pypi status]: https://pypi.org/project/FunctionalPy/
[tests]: https://github.com/MartinBernstorff/FunctionalPy/actions?workflow=Tests
[dev container]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/FunctionalPy/


<!-- start short-description -->
Python has implemented `map`, `filter` etc. as functions, rather than methods on a sequence. This makes the result harder to read and Iterators less used than they could be. FunctionalPy exists to change that. 

You get this 🔥:

```python
result = (Seq([1,2,3])
            .map(multiply_by_2)
            .filter(is_even)
            )
```

Instead of this:

```python
sequence = [1,2,3]
multiplied = [multiply_by_2(x) for x in sequence]
result = [x for x in multiplied if is_even(x)]
```

Or this:

```python
result = filter(is_even, map(multiply_by_2, [1,2,3]))
```
<!-- end short-description -->

## Install
```bash
pip install functionalpy
```

## Usage
```python
from functionalpy import Seq

result = (Seq([1, 2])
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * 2)
            .to_list()
)
assert result == [4]
```

## Philosophy
* Make it work: Concise syntax borrowed from Scala, Rust etc.
* Make it right: Fully typed, no exceptions
* Make it fast: Concurrency through `.pmap`, potentially caching in the future
* Keep it simple: No dependencies

## Prior art
FunctionalPy stands on the shoulders of Scala, Rust etc. 

Moreover, [PyFunctional](https://github.com/EntilZha/PyFunctional) has existed for 7+ years with a comprehensive feature set. It is performant, with built-in lineage and caching. Unfortunately, this makes typing [non-trivial, with a 4+ year ongoing effort to add types](https://github.com/EntilZha/PyFunctional/issues/118).

## Contributing
#### Devcontainer
1. Install [Orbstack](https://orbstack.dev/) or Docker Desktop. Make sure to complete the full install process before continuing.
2. If not installed, install VSCode
3. Press this [link](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/FunctionalPy/)
4. Complete the setup process
5. Done! Easy as that.

## 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |

[github issue tracker]: https://github.com/MartinBernstorff/FunctionalPy/issues
[github discussions]: https://github.com/MartinBernstorff/FunctionalPy/discussions



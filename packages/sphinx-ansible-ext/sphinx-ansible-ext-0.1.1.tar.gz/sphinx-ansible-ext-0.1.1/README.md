[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/twiddle-z/sphinx-ansible-ext/badges/master/pipeline.svg)](https://gitlab.com/twiddle-z/sphinx-ansible-ext/pipelines)
[![coverage](https://gitlab.com/twiddle-z/sphinx-ansible-ext/badges/master/coverage.svg)](https://gitlab.com/twiddle-z/sphinx-ansible-ext/coverage/index.html)

# Sphinx Ansible extension

Sphinx documentation Ansible directives and yaml2rst


## Installation

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U sphinx-ansible-ext
~~~


## Usage

* `conversions.yaml2rst_role_defaults(search_path, dst_path, filename="main.yml", *, force=False)`

Searches through `search_path` for `defaults/<filename.yml` and converts the yaml file to rst.

* directive `ansible-var-desc`

Builds a table to describe the variables. Input format is:

```
variable
  type [/ required]
  Help string
```

Example:

```
username
  string / required
  The username.
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Locations

  * Documentation: [https://gitlab.com/twiddle-z/sphinx-ansible-ext](https://gitlab.com/twiddle-z/sphinx-ansible-ext)
  * Website: [https://gitlab.com/twiddle-z/sphinx-ansible-ext](https://gitlab.com/twiddle-z/sphinx-ansible-ext)
  * PyPi: [https://pypi.org/project/sphinx-ansible-ext](https://pypi.org/project/sphinx-ansible-ext)

DMC VIEW

Digital Magnatic Compass View

.. start-badges

| |build| |release_version| |wheel| |supported_versions|
| |docs| |coverage| |maintainability| |tech-debt|
| |ruff| |gh-lic| |commits_since_specific_tag_on_main| |commits_since_latest_github_release|

|
| **Code:** https://github.com/alanmehio/dmc-view
| **Docs:** https://dmc-view.readthedocs.io/en/main/
| **PyPI:** https://pypi.org/project/dmc-view/
| **CI:** https://github.com/alanmehio/dmc-view/actions/


Features
========

1. **dmc_view** `python package`

   a. View Object Azimuth and Inclindation; also View Declination(Offset from real North)  **Create Feature**
   b. Circule view animation  **Nice Feature**
2. Tested against multiple `platforms` and `python` versions


Development
-----------

| Get started: 
| Insall `pip` 
 
.. code-block:: shell

    python3 -m pip install 


Install `Pyside6` 

.. code-block:: shell

    pip install  Py

Install `tox` 

.. code-block:: shell

    pip install  tox

Then, to see all out-of-the-box available `tox` commands:

.. code-block:: shell

    tox -a
    

OR **`tox -av`** for showing `description` of each command

Development Notes
~~~~~~~~~~~~~~~~~
Testing, Documentation Building, Scripts, CI/CD, Static Code Analysis for this project.

1. **Test Suite**, using `pytest`_, located in `tests` dir
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir
4. **CI/CD Pipeline**, running on `Github Actions`_, defined in `.github/`

   a. **Test Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`, `windows-latest`
      2. Python Interpreters: `3.8`, `3.9`, `3.10`, `3.11`
   b. **Continuous Deployment**
   
      `Production`
      
         1. **Python Distristribution** to `pypi.org`_, on `tags` **v***, pushed to `main` branch
         2. **Docker Image** to `Dockerhub`_, on every push, with automatic `Image Tagging`
      
      `Staging`

         1. **Python Distristribution** to `test.pypi.org`_, on "pre-release" `tags` **v*-rc**, pushed to `release` branch

   c. **Configurable Policies** for `Docker`, and `Static Code Analysis` Workflows
5. **Automation**, using `tox`_, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using the fast `Ruff`_ linter, along with `isort`_ and `black`_


Prerequisites
=============

You need to have `Python` and  `PySide6`  installed.

Quickstart
==========

Using `pip` is the approved way for installing `dmc_view`.

.. code-block:: sh

    python3 -m pip install dmc_view


TODO Document a use case TODO Alan usage here 


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


License
=======

* Free software: GNU Affero General Public License v3.0



.. LINKS

.. _tox: https://tox.wiki/en/latest/

.. _pytest: https://docs.pytest.org/en/7.1.x/

.. _build: https://github.com/pypa/build

.. _Dockerhub: https://hub.docker.com/

.. _pypi.org: https://pypi.org/

.. _test.pypi.org: https://test.pypi.org/

.. _mypy: https://mypy.readthedocs.io/en/stable/

.. _Ruff: https://docs.astral.sh/ruff/

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/

.. _Github Actions: https://github.com/alanmehio/dmc-view/actions

.. _GNU Affero General Public License v3.0: https://github.com/alanmehio/dmc-view/blob/main/LICENSE


.. BADGE ALIASES

.. Build Status
.. Github Actions: Test Workflow Status for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/alanmehio/dmc-view/Test%20Python%20Package/main?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/alanmehio/dmc-view/actions/workflows/test.yaml?query=branch%3Amain


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/dmc-view/main?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://dmc-view.readthedocs.io/en/main/

.. Code Coverage

.. |coverage| image:: https://img.shields.io/codecov/c/github/alanmehio/dmc-view/main?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/alanmehio/dmc-view

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/dmc_view
    :alt: Production Version
    :target: https://pypi.org/project/dmc-view/

.. |wheel| image:: https://img.shields.io/pypi/wheel/dmc-view?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/dmc-view

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/dmc-view?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/dmc-view

.. Github Releases & Tags

.. |commits_since_specific_tag_on_main| image:: https://img.shields.io/github/commits-since/alanmehio/dmc-view/v0.0.1/main?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/alanmehio/dmc-view/compare/v0.0.1..main

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/alanmehio/dmc-view/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/github/license/alanmehio/dmc-view
    :alt: GitHub
    :target: https://github.com/alanmehio/dmc-view/blob/main/LICENSE


.. CODE QUALITY

.. Ruff linter for Fast Python Linting

.. |ruff| image:: https://img.shields.io/badge/codestyle-ruff-000000.svg
    :alt: Ruff
    :target: https://docs.astral.sh/ruff/

.. Code Climate CI
.. Code maintainability & Technical Debt

.. |maintainability| image:: https://img.shields.io/codeclimate/maintainability/alanmehio/dmc-view
    :alt: Code Climate Maintainability
    :target: https://codeclimate.com/github/alanmehio/dmc-view

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/alanmehio/dmc-view
    :alt: Technical Debt
    :target: https://codeclimate.com/github/alanmehio/dmc-view

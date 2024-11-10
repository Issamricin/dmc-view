===========
Development
===========

| Insall `pip` 
 
.. code-block:: shell

    python3 -m pip install 


| Install `Pyside6` 

.. code-block:: shell

    pip install  PySide6

| Install `tox` 

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
4. **CI(Continuous Integration)/CD(Continuous Delivery) Pipeline**, running on `Github Actions`, defined in `.github/`

   a. **Test Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`, `windows-latest`
      2. Python Interpreters: `3.8`, `3.9`, `3.10`, `3.11`
   b. **Continuous Deployment**
   
      `Production`
      
         1. **Python Distristribution** to `pypi.org`_, on `tags` **v***, pushed to `main` branch
         2. **Docker Image** to `Dockerhub`_, on every push, with automatic `Image Tagging`
      
      `Staging`

         3. **Python Distristribution** to `test.pypi.org`_, on "pre-release" `tags` **v*-rc**, pushed to `release` branch

   c. **Configurable Policies** for `Docker`, and `Static Code Analysis` Workflows
5. **Automation**, using `tox`_, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using the fast `Ruff`_ linter, along with `isort`_ and `black`_


Prerequisites
-------------

You need to have `Python` and  `PySide6`  installed for Development


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

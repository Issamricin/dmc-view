"""Run `python -m dmc_view`.

Allow running DMC View, also by invoking
the python module:

`python -m dmc_view`

This is an alternative to directly invoking the cli that uses python as the
"entrypoint".
"""

from __future__ import absolute_import

from dmc_view.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name="dmc-view")  # pylint: disable=unexpected-keyword-arg

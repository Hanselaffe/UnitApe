"""Backward-compatible entry point for the historical UnitApe filename."""

from unitape_core import *  # noqa: F401,F403
from unitape_core import main


if __name__ == "__main__":
    raise SystemExit(main())

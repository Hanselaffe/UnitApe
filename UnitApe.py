"""Backward-compatible entry point for the historical UnitApe filename."""

from unitape import *  # noqa: F401,F403
from unitape import main


if __name__ == "__main__":
    raise SystemExit(main())

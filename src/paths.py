from pathlib import Path


def package_root() -> Path:
    """Return the coding-spec toolkit root directory."""
    return Path(__file__).resolve().parent.parent
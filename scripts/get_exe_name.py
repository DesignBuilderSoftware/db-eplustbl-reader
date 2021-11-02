"""
Script to create platform and current version dependent executable name.

"""
import platform
from pathlib import Path


def get_version_from_toml() -> str:
    """Extract current version information from pyproject file."""
    with open(Path(Path(__file__).parents[1], "pyproject.toml"), mode="r") as toml_file:
        for line in toml_file:
            if "version" in line:
                quoted_version = line.split("=")[1].strip()
                version = quoted_version.replace('"', "")
                return version
    raise ValueError("Cannot find version info in pyproject.toml")


def create_name():
    """Create application executable detailed name."""
    current_version = get_version_from_toml()
    platform_info = platform.platform()
    name = f"db-temperature-distribution {current_version} {platform_info}"
    return name


if __name__ == "__main__":
    print(create_name())

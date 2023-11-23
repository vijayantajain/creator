"""Module to load and validate configurations"""

from pathlib import Path
from typing import Union
from dynaconf import Dynaconf, Validator


def path_exists(path: Union[str, Path]):
    """The path exists"""
    return Path(path).exists()


def dir_exists(dirpath: Union[str, Path]):
    """The path is a directory and it exists"""
    return path_exists(dirpath) and Path(dirpath).is_dir()


def is_valid_label(label: str):
    """Label is one of three values"""
    return label in ["privacy_practice", "purpose", "information_acccessed"]


settings = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=["../.config/basic_config.toml"]
)

settings.validators.register(
    # Extract section
    Validator("extract.filepath", must_exist=True, condition=path_exists),
    Validator("extract.n_hops", must_exist=True, is_type_of=int, gte=1, lte=3),
    Validator("extract.label", must_exist=True, condition=is_valid_label),
    Validator("extract.output_dir", must_exist=True),
    # Mine section
    Validator("mine.num_of_threads", is_type_of=int),
    # Create section
    Validator("create.output_filepath", must_exist=True),
)


settings.validators.validate()

"""Module to define config model and validate"""

from pathlib import Path
from typing import Union
from pydantic import BaseModel, FilePath, DirectoryPath, validator

__all__ = ["ExtractCfgModel", "MineCfgModel", "CreateCfgModel"]


def path_exists(path: Union[str, Path]):
    """The path exists"""
    return Path(path).exists()


def dir_exists(dirpath: Union[str, Path]):
    """The path is a directory and it exists"""
    return path_exists(dirpath) and Path(dirpath).is_dir()


class ExtractCfgModel(BaseModel):
    """Config model for Extract"""

    filepath: FilePath
    n_hops: int
    label: str
    output_dir: Union[str, Path]

    @validator("label")
    @classmethod
    def is_valid_label(cls, v: str) -> str:
        """Label is one of three values"""
        if v not in ["privacy_practice", "purpose", "information_acccessed"]:
            raise ValueError(
                "'label' must either be 'privacy_practice', 'purpose', or 'information_accessed'"
            )
        return v

    @validator("n_hops")
    @classmethod
    def valid_num_hops(cls, v: int) -> int:
        """There are only upto 3 hops"""
        if (1 > v) and (v > 3):
            raise ValueError("'n_hops' should be between 1 and 3")
        return v


class MineCfgModel(BaseModel):
    """Config model for PathMiner"""

    cli_dir: DirectoryPath
    output_dir: Union[str, Path]
    num_of_threads: int
    config_path: Union[str, Path]
    parser: dict
    label: dict
    storage: dict


class CreateCfgModel(BaseModel):
    """Config model for Create"""

    output_filepath: Union[str, Path]
    delimiter: str

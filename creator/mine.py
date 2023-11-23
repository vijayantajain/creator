"""Module to create AST paths from astminer"""

import os
from pathlib import Path
from typing import Union
import yaml


class PathMiner:
    """Wrapper class that executes astminer to create AST paths"""

    def __init__(
        self,
        cli_path: Union[str, Path],
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        parser: dict,
        label: dict,
        storage: dict,
        num_threads: int,
        config_path: Union[str, Path],
    ) -> None:
        self.cli_path = cli_path
        self.input_dir = str(Path(input_dir).absolute())
        self.output_dir = str(Path(output_dir).absolute())
        self.parser = parser
        self.label = label
        self.storage = storage
        self.num_threads = num_threads
        self.config_path = str(Path(config_path).absolute())

    def create_config_file(self):
        """Create yaml config file for astminer"""
        config = {}

        config["inputDir"] = self.input_dir
        config["outputDir"] = self.output_dir
        config["parser"] = dict(self.parser)
        config["label"] = dict(self.label)
        config["storage"] = self.storage
        config["numOfThreads"] = int(self.num_threads)

        with open(self.config_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file)

    def create_ast_paths(self) -> None:
        """Runs cli.sh in astminer"""
        CWD = Path.cwd()
        os.chdir(self.cli_path)
        os.system(f"./cli.sh {self.config_path}")
        os.chdir(CWD)

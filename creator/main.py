"""Module creates the necessary objects and creates the dataset"""

from pathlib import Path

from extract import Extract
from mine import PathMiner
from create import Create

from validator import *

import json

with open(".config/config.json", "r", encoding="utf-8") as file:
    configs = json.load(file)


# Extract src code into .java files
ext_cfg = ExtractCfgModel(**configs["extract_cfg"])

java_extractor = Extract(
    ext_cfg.filepath, ext_cfg.n_hops, ext_cfg.label, ext_cfg.output_dir
)

java_files_dir = java_extractor.extract_src_code_into_java_files()

# Mine AST Paths
mine_cfg = MineCfgModel(**configs["mine_cfg"])

path_miner = PathMiner(
    cli_path=mine_cfg.cli_dir,
    input_dir=java_files_dir,
    output_dir=mine_cfg.output_dir,
    parser=mine_cfg.parser,
    label=mine_cfg.label,
    storage=mine_cfg.storage,
    num_threads=mine_cfg.num_of_threads,
    config_path=mine_cfg.config_path,
)

path_miner.create_config_file()
path_miner.create_ast_paths()

# Create dataset file
output_dir = Path(path_miner.output_dir).joinpath("java")
create_cfg = CreateCfgModel(**configs["create_cfg"])


creator = Create(
    output_dir=output_dir,
    output_filepath=create_cfg.output_filepath,
    delimiter=create_cfg.delimiter,
)

creator.create_dataset()

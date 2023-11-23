"""Module creates the necessary objects and creates the dataset"""

from extract import Extract
from config import settings

ext_cfg = settings.extract

java_extractor = Extract(
    ext_cfg.filepath, ext_cfg.n_hops, ext_cfg.label, ext_cfg.output_dir
)


java_files_dir = java_extractor.extract_src_code_into_java_files()

"""Module to extract data from JSON and save it in JAVA file"""

import os
import re
import json
from pathlib import Path
from typing import Union


class Extract:
    """Class to extract java source code from JSON file into individual .java files"""

    def __init__(
        self,
        data_filepath: str,
        n_hops: int,
        label: str,
        out_dirpath: Union[str, Path],
    ):
        self.filepath = data_filepath
        self.n_hops = n_hops
        self.label = label
        self.out_dirpath = out_dirpath

    @staticmethod
    def get_src_code(methods: list, n_hops: int) -> str:
        """Combines the methods into a single string and then returns them"""

        combined_code = ""

        for i in range(n_hops):
            try:
                code = methods[i]["src_code"]
                end_index = re.search(r"\*/", code).span()[-1]
                combined_code += code[end_index:] + "\n"
            except IndexError:
                break

        return combined_code

    @staticmethod
    def write_to_file(filepath: Union[str, Path], src_code: str) -> None:
        """Writes the `src_code` to `filepath`"""

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(src_code)

    def extract_src_code_into_java_files(self):
        """Main method to extract source code from json file and write them as java files"""
        # Create output directory

        dest_dirpath = Path(self.out_dirpath)

        if not Path(dest_dirpath).exists():
            os.makedirs(dest_dirpath)

        # Load data
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract src_code from each annotation and save them as .java file
        for i, each_prcs in enumerate(data):
            try:
                data_id = each_prcs["dataId"]
                src_code = Extract.get_src_code(
                    each_prcs["data"]["methods"], self.n_hops
                )
                if self.label != "information_accessed":
                    try:
                        label = each_prcs["data"]["labels"][self.label][0]["label"]
                    except IndexError:
                        pass
                else:
                    label = each_prcs["data"]["labels"][self.label][0]["label"]

                dest_filepath = dest_dirpath.joinpath(f"{label}_{data_id}.java")

                Extract.write_to_file(dest_filepath, src_code)
            except Exception as e:
                print(f"Exception has occurred at index: {i}. {e}")

        return dest_dirpath

"""Module that creates dataset text file"""

from pathlib import Path
from typing import Union


class Create:
    """Creates dataset object by parsing AST paths"""

    def __init__(
        self,
        output_dir: Union[str, Path],
        output_filepath: Union[str, Path],
        delimiter: str,
    ) -> None:
        self.output_dir = Path(output_dir).absolute()
        self.paths_file = self.output_dir.joinpath("data/path_contexts.c2s")
        self.output_filepath = Path(output_filepath).absolute()
        self.node_token_dict = Create.get_token_dict(
            self.output_dir.joinpath("node_types.csv")
        )
        self.delimiter = delimiter

    @staticmethod
    def get_token_dict(node_token_filepath: Union[str, Path]):
        """Parses node_type.csv file and saves the id as a dictionary"""
        with open(node_token_filepath, "r", encoding="utf-8") as file:
            data = file.readlines()

            file_dict = {}

        data = data[1:]  # skip the header column

        for el in data:
            token_id, obj = el.split(",")
            file_dict[token_id.strip()] = obj.strip()

        return file_dict

    def create_dataset(self):
        """Method to create dataset file"""
        samples = []
        with open(self.paths_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i, each_line in enumerate(lines):
            first_part, paths = each_line.split(" ", 1)

            label = first_part.split("_", 1)[0]
            sample_id = first_part.split("_", 1)[-1].split(".")[0]

            list_of_paths = paths.split(" ")

            new_sample = []

            for j, each_path in enumerate(list_of_paths):
                start_node, non_terminal_nodes, end_node = each_path.split(",")
                decoded_non_terminal_path = "|".join(
                    [
                        self.node_token_dict[f]
                        for f in non_terminal_nodes.split(self.delimiter)
                    ]
                )
                new_path = f"{start_node}{self.delimiter}{decoded_non_terminal_path}{self.delimiter}{end_node.strip()}"
                new_sample.append(new_path)
            all_paths = " ".join(new_sample)
            samples.append(f"{sample_id}###{all_paths}###{label}")

        with open(self.output_filepath, "w", encoding="utf-8") as file:
            for i, each_sample in enumerate(samples):
                file.write(each_sample + "\n")

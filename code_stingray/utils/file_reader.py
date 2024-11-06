# Copyright 2024 Mansun Kuo

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


class FileReader:
    """
    A class to read all files and folders under a given path, ignoring binary files.
    """

    def __init__(self, path: str):
        """
        Initializes the FileReader with the given path.

        Args:
            path (str): The path to the file or directory to read.
        """
        self.path = path

    def read(self) -> list:
        """
        Reads all files and folders under the given path.

        Returns:
            list: A list of tuples, where each tuple contains:
                - The type of the item ("file" or "directory").
                - The full path to the item.
                - The content of the item (for files) or None (for directories).
        """
        items = []
        if os.path.isfile(self.path):
            self._read_file(self.path, items)
        elif os.path.isdir(self.path):
            for root, _, files in os.walk(self.path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self._read_file(file_path, items)
                for dir_path in os.listdir(root):
                    full_dir_path = os.path.join(root, dir_path)
                    if os.path.isdir(full_dir_path):
                        items.append(("directory", full_dir_path, None))
        else:
            raise ValueError(f"Invalid path: {self.path}")
        return items

    def _read_file(self, file_path: str, items: list) -> None:
        """
        Reads a single file and appends its information to the items list.

        Args:
            file_path (str): The path to the file.
            items (list): The list to append the file information to.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            items.append(("file", file_path, content))
        except UnicodeDecodeError:
            # Ignore binary files
            pass

    def read_and_concat_files(self) -> str:
        """
        Reads all files under the given path, concatenates their content with
        file paths, and returns the result as a single string.

        Returns:
            str: A string containing the concatenated content of all files,
                 with each file's content preceded by its path.
        """
        concatenated_content = ""
        items = self.read()
        for item_type, item_path, content in items:
            if item_type == "file" and content:
                concatenated_content += f"Path: {item_path} Content:\n{content}\n\n"
        return concatenated_content


if __name__ == "__main__":
    reader = FileReader("code_stingray/utils")
    concatenated_result = reader.read_and_concat_files()
    print(concatenated_result)

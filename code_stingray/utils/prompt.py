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

from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)
import yaml


class Prompt:
    def __init__(self, file_path: str = ""):
        self.file_path = self._get_file_path(file_path)
        self._data = self.load_yaml()

    @staticmethod
    def _get_file_path(file_path: str) -> str:
        """Gets the path to the prompt.yaml file."""
        if file_path:
            return file_path
        else:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../config/prompt.yaml")
            )

    def load_yaml(self) -> dict:
        """Loads the YAML file and returns its content as a dictionary."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    @property
    def review_instructions(self) -> str:
        return self._data["review"]["instructions"]

    @property
    def review_output_format(self) -> str:
        return self._data["review"]["output_format"]

    @property
    def review_examples(self):
        return self._data["review"]["examples"]

    def get_few_shot_prompt(self) -> FewShotChatMessagePromptTemplate:
        """Returns the few-shot prompt from the loaded YAML data."""
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{query}"),
                ("ai", "{response}"),
            ]
        )
        examples = self.review_examples
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
        )

        return few_shot_prompt

    def get_review_prompt(self, system_as_human: bool = False) -> ChatPromptTemplate:
        review_prompt = ChatPromptTemplate(
            [
                ("system", self.review_instructions),
                ("system", self.review_output_format),
                self.get_few_shot_prompt(),
                ("human", "{code}"),
            ]
        )
        # TODO: remove system_as_human when ChatGoogleGenerativeAI works with system prompt
        # https://github.com/langchain-ai/langchainjs/issues/5069
        if system_as_human:
            review_prompt = ChatPromptTemplate(
                [
                    ("human", self.review_instructions),
                    ("human", self.review_output_format),
                    self.get_few_shot_prompt(),
                    ("human", "{code}"),
                ]
            )

        return review_prompt

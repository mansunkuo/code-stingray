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

import getpass
import os

from langchain_openai import ChatOpenAI

from code_stingray.llms.llm import LLM


class OpenAILLM(LLM):
    """Concrete LLM class for Google Vertex AI."""

    def __init__(self, model_name, **kwargs):
        super().__init__(model_name)

    def create(self) -> ChatOpenAI:
        if os.getenv("OPENAI_API_KEY") is None:
            os.environ["OPENAI_API_KEY"] = getpass.getpass(
                "Enter your OpenAI API Key: "
            )
        return ChatOpenAI(model=self.model_name)

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

from code_stingray.llms.google_ai import GoogleAILLM
from code_stingray.llms.google_cloud import GoogleCloudLLM
from code_stingray.llms.openai import OpenAILLM


class LLMFactory:
    _providers = {
        "google_ai": GoogleAILLM,
        "google_cloud": GoogleCloudLLM,
        "openai": OpenAILLM,
    }

    @staticmethod
    def create(provider: str, model_name: str, **kwargs):
        provider = provider.lower()
        llm_class = LLMFactory._providers.get(provider)
        if not llm_class:
            raise ValueError(f"Invalid provider: {provider}")
        return llm_class(model_name, **kwargs).create()

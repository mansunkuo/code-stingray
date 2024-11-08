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
    @staticmethod
    def create(provider: str, model_name: str, **kwargs):
        provider = provider.lower()
        if provider == "google_ai":
            return GoogleAILLM(model_name, **kwargs).create()
        elif provider == "google_cloud":
            return GoogleCloudLLM(model_name, **kwargs).create()
        elif provider == "openai":
            return OpenAILLM(model_name, **kwargs)
        else:
            raise ValueError("Invalid provider.")

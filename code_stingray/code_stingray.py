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

from code_stingray.utils.prompt import Prompt
from code_stingray.utils.git import Git
from code_stingray.utils.file_reader import FileReader


class CodeStingray:
    def __init__(self, llm):
        self.prompt = Prompt()
        self.llm = llm

    def _get_code_from_local(
        self, path: str, commit1: str = None, commit2: str = None
    ) -> str:
        """Retrieves code from a local path, optionally using Git diff."""
        reader = FileReader(path)
        code = reader.read_and_concat_files()
        if commit1 and commit2:
            git = Git(repo_path=path)
            code = git.get_diff(commit1=commit1, commit2=commit2)
        return code

    def _get_code_from_remote_git(
        self, remote_url: str, remote_branch: str, commit1: str, commit2: str
    ) -> str:
        """Retrieves code from a remote Git repository using diff."""
        git = Git(remote_url=remote_url, remote_branch=remote_branch)
        code = git.get_diff(commit1=commit1, commit2=commit2)
        return code

    def review(
        self,
        path: str = None,
        remote_url: str = None,
        remote_branch: str = None,
        commit1: str = None,
        commit2: str = None,
    ):
        # TODO: remove system_as_human when ChatGoogleGenerativeAI works with system prompt
        # https://github.com/langchain-ai/langchainjs/issues/5069
        system_as_human = False
        if self.llm.get_name() == "ChatGoogleGenerativeAI":
            system_as_human = True
        review_prompt = self.prompt.get_review_prompt(system_as_human=system_as_human)

        # pylint: disable=unsupported-binary-operation
        chain = review_prompt | self.llm

        if path:
            code = self._get_code_from_local(path, commit1, commit2)
        elif remote_url:
            code = self._get_code_from_remote_git(
                remote_url, remote_branch, commit1, commit2
            )
        else:
            raise ValueError("Either 'path' or 'remote_url' must be provided.")

        result = chain.invoke(code)
        return result

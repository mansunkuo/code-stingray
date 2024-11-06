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

import subprocess
import tempfile
import shutil
from typing import Optional


class Git:
    """
    A class to interact with Git repositories and retrieve diffs between commits
    using the Git CLI.
    """

    def __init__(
        self,
        repo_path: Optional[str] = None,
        remote_url: Optional[str] = None,
        remote_branch: Optional[str] = None,
    ):
        """
        Initializes the Git object.

        Args:
            repo_path (str, optional): Path to the local Git repository.
                                        Defaults to None.
            remote_url (str, optional): URL of the remote Git repository.
                                        Defaults to None.
                                        If a remote URL is provided, the Git
                                        repository will be cloned to a temporary
                                        directory and deleted upon object
                                        destruction.
            remote_branch (str, optional): Branch to clone from the remote
                                            repository. Defaults to None, which
                                            clones the default branch.

        Raises:
            ValueError: If both `repo_path` and `remote_url` are provided,
                         or neither is provided.
        """

        if repo_path and remote_url:
            raise ValueError(
                "Both 'repo_path' and 'remote_url' are provided. "
                "Please provide only one."
            )
        if not repo_path and not remote_url:
            raise ValueError("Either 'repo_path' or 'remote_url' must be provided.")

        self.repo_path = repo_path if repo_path else tempfile.mkdtemp()
        self.remote_url = remote_url
        self.remote_branch = remote_branch
        if self.remote_url:
            self._clone_repo()

    def _clone_repo(self) -> None:
        """Clones the remote repository to a temporary directory."""
        command = [
            "git",
            "clone",
            self.remote_url,
            self.repo_path,
        ]
        if self.remote_branch:
            command.extend(["-b", self.remote_branch])
        self._run_command(command)

    def _run_command(self, command: list[str]) -> str:
        """
        Runs a command using subprocess.

        Args:
            command (list): The Git command to run as a list of strings.

        Returns:
            str: The output of the command.

        Raises:
            RuntimeError: If the Git command fails.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}") from e

    def get_diff(self, commit1: str, commit2: str) -> str:
        """
        Gets the diff between two commits using the Git CLI.
        git diff commit1 commit2
        commit1 is supposed to be an older one.

        Args:
            commit1 (str): The first commit hash or reference.
            commit2 (str): The second commit hash or reference.

        Returns:
            str: The diff between the two commits.
        """
        self._run_command(
            ["git", "-C", self.repo_path, "fetch", "origin", commit1, commit2]
        )
        diff = self._run_command(
            ["git", "-C", self.repo_path, "diff", commit1, commit2]
        )
        return diff

    def __del__(self):
        if self.remote_url:
            shutil.rmtree(self.repo_path)


if __name__ == "__main__":
    git = Git(
        remote_url="git@github.com:mansunkuo/k8s-summit-2024.git", remote_branch="main"
    )
    print(
        git.get_diff(
            "e1fa0a3406f93edd5cd334a7cf98780478b0b501",
            "0ab5dafc939c2672b2eac57b674aa5c1c39f2159",
        )
    )

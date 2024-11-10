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

from argparse import ArgumentParser
import sys
import os


def get_args():
    parser = ArgumentParser()
    path_remote_group = parser.add_mutually_exclusive_group(required=True)
    path_remote_group.add_argument(
        "--path",
        "-p",
        type=str,
        help="Path to the local Git repository, a file or directory",
    )
    path_remote_group.add_argument(
        "--remote_url",
        "-ru",
        type=str,
        help="URL of the remote Git repository",
    )
    parser.add_argument(
        "--remote_branch",
        "-rb",
        type=str,
        default=None,
        help="Branch to clone from the remote repository",
    )
    parser.add_argument(
        "--commit1",
        "-c1",
        type=str,
        default=None,
        help="First commit hash of 'git diff commit1 commit2'",
    )
    parser.add_argument(
        "--commit2",
        "-c2",
        type=str,
        default=None,
        help="Second commit hash of 'git diff commit1 commit2'",
    )

    # llm
    llm_parsers = parser.add_subparsers(dest="llm", help="Available LLM")

    # google ai
    google_cloud_parser = llm_parsers.add_parser("google_ai", help="Google AI LLM")
    google_cloud_parser.add_argument(
        "--model", type=str, default="gemini-1.5-pro", help="LLM model name"
    )

    # google cloud vertex ai
    google_cloud_parser = llm_parsers.add_parser(
        "google_cloud", help="Google Cloud Vertex AI LLM"
    )
    google_cloud_parser.add_argument(
        "--model", type=str, default="gemini-1.5-pro", help="LLM model name"
    )
    google_cloud_parser.add_argument(
        "--google_cloud_project", type=str, help="Google Cloud Project"
    )
    google_cloud_parser.add_argument(
        "--google_cloud_location",
        default="us-west1",
        type=str,
        help="Google Cloud Location (default: %(default)s))",
    )

    # # openai
    # openai_parser = llm_parsers.add_parser("openai", help="OpenAI LLM")
    # openai_parser.add_argument(
    #     "--model", type=str, default="gpt-4", help="LLM model name"
    # )

    # Git platform
    for llm_parser in llm_parsers.choices.values():
        cicd_parsers = llm_parser.add_subparsers(
            dest="git_platform", help="Git platform"
        )
        github_parser = cicd_parsers.add_parser("github", help="GitHub")
        github_parser.add_argument(
            "--github_token",
            type=str,
            default=os.environ.get("GITHUB_TOKEN"),
            help="GitHub personal access token",
        )
        github_parser.add_argument(
            "--github_repo_owner", type=str, help="GitHub repository owner"
        )
        github_parser.add_argument(
            "--github_repo_name", type=str, help="GitHub repository name"
        )
        github_parser.add_argument(
            "--github_pr_number", type=int, help="GitHub pull request number"
        )

    args = parser.parse_args()

    if not args.llm:
        parser.print_help()
        sys.exit(1)

    # Check if commit1 and commit2 are both provided or both None
    if (args.commit1 is None) != (args.commit2 is None):  # XOR condition
        parser.error(
            "Both --commit1 (-c1) and --commit2 (-c2) must be provided together, or neither should be provided."
        )

    return args


if __name__ == "__main__":
    cli_args = get_args()
    print(cli_args)

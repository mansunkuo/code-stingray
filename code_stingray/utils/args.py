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

    # google
    google_parser = llm_parsers.add_parser("google", help="Google LLM")
    google_parser.add_argument(
        "--model", type=str, default="gemini-1.5-flash", help="LLM model name"
    )
    google_parser.add_argument("--google_project", type=str, help="Google Project")
    google_parser.add_argument(
        "--google_location",
        default="us-west1",
        type=str,
        help="Google Location (default: %(default)s))",
    )

    # # openai
    # openai_parser = llm_parsers.add_parser("openai", help="OpenAI LLM")
    # openai_parser.add_argument(
    #     "--model", type=str, default="gpt-4", help="LLM model name"
    # )

    # cicd
    for llm_parser in llm_parsers.choices.values():
        cicd_parsers = llm_parser.add_subparsers(dest="cicd", help="Available CI/CD")
        cicd_parsers.add_parser("cloudbuild", help="Cloudbuild CI/CD")
        cicd_parsers.add_parser("github_actions", help="Github CI/CD")

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

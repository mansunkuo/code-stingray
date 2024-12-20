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

from code_stingray.utils.args import get_args
from code_stingray.code_stingray import CodeStingray
from code_stingray.llms.llm_factory import LLMFactory
from code_stingray.git_platform.commenter_factory import CommenterFactory
from code_stingray.utils.logging import logger


def main():
    args = get_args()
    logger.setLevel(args.log_level)
    logger.debug(args)
    llm = LLMFactory.create(args.llm, args.model, **vars(args))
    code_stingray = CodeStingray(llm)
    result = code_stingray.review(
        path=args.path,
        remote_url=args.remote_url,
        remote_branch=args.remote_branch,
        commit1=args.commit1,
        commit2=args.commit2,
    )
    logger.debug(result)
    logger.info(result.content)

    if args.git_platform:
        commenter = CommenterFactory.create(args.git_platform, **vars(args))
        commenter.add_comment(result.content)


# Example Usage:
if __name__ == "__main__":
    main()

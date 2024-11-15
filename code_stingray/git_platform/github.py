from github import Github
from github import GithubException

from code_stingray.git_platform.commenter import Commenter
from code_stingray.utils.logging import logger


class GithubCommenter(Commenter):
    """Adds comments to GitHub pull requests."""

    def __init__(self, **kwargs):
        """Initializes the GithubCommenter.

        Args:
            **kwargs: Keyword arguments containing:
                github_repo_owner (str): The owner of the GitHub repository.
                github_repo_name (str): The name of the GitHub repository.
                github_pr_number (int): The number of the pull request.
                github_token (str): The GitHub personal access token.

        Raises:
            ValueError: If neither 'token', nor both 'private_key_path' and 'app_id' are provided.
        """

        self.repo_owner = kwargs.get("github_repo_owner")
        self.repo_name = kwargs.get("github_repo_name")
        self.pr_number = kwargs.get("github_pr_number")
        self.token = kwargs.get("github_token")

        self.github = Github(self.token)
        self.repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")

    def add_comment(self, comment_body: str) -> None:
        """
        Add a comment to a GitHub pull request.

        Args:
            comment_body (str): The text of the comment to add.
        """
        try:
            pr = self.repo.get_pull(number=self.pr_number)
            pr.create_issue_comment(comment_body)
        except GithubException as e:
            logger.error("Failed to add comment to GitHub: %s", e)
            # Consider raising the exception or handling it differently based on your needs
            # raise  # Re-raise the exception if necessary
        except Exception as e:
            logger.exception(
                "An unexpected error occurred while adding a comment: %s", e
            )
            # raise  # Re-raise if you want other parts of your code to handle it.

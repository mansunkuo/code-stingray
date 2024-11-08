from abc import ABC, abstractmethod

from github import Github  # Import github library here


class Commenter(ABC):
    """Abstract base class for adding comments to pull requests."""

    @abstractmethod
    def add_comment(self, pr_number: int, comment_body: str) -> None:
        """
        Add a comment to a pull request.

        Args:
            pr_number (int): The number of the pull request.
            comment_body (str): The text of the comment to add.
        """
        raise NotImplementedError("Subclasses must implement add_comment()")


class GithubCommenter(Commenter):
    """Adds comments to GitHub pull requests."""

    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        Initializes the GithubPullRequestCommenter.

        Args:
            token (str): Your GitHub personal access token with appropriate permissions.
            repo_owner (str): The owner of the repository.
            repo_name (str): The name of the repository.
        """

        self.github = Github(token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")

    def add_comment(self, pr_number: int, comment_body: str) -> None:
        """
        Add a comment to a GitHub pull request.

        Args:
            pr_number (int): The number of the pull request.
            comment_body (str): The text of the comment to add.
        """
        pr = self.repo.get_pull(number=pr_number)
        pr.create_issue_comment(comment_body)

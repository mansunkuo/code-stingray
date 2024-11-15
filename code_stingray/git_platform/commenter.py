from abc import ABC, abstractmethod


class Commenter(ABC):
    """Abstract base class for adding comments to pull requests."""

    @abstractmethod
    def add_comment(self, comment_body: str) -> None:
        """
        Add a comment to a pull request.

        Args:
            comment_body (str): The text of the comment to add.
        """
        raise NotImplementedError("Subclasses must implement add_comment()")

from code_stingray.git_platform.github import GithubCommenter


class CommenterFactory:
    _providers = {
        "github": GithubCommenter,
    }

    @staticmethod
    def create(provider: str, **kwargs):
        commenter_class = CommenterFactory._providers.get(provider.lower())
        if not commenter_class:
            raise ValueError(f"Invalid git_platform: {provider}")
        return commenter_class(**kwargs)

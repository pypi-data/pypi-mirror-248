from typing import Optional

from github.Branch import Branch
from github.GitCommit import GitCommit
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from github.PullRequestReview import PullRequestReview
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class PullRequestReviewEvent(Event):
    """This class represents a pull request review event."""

    event_identifier = {"event": "pull_request_review"}

    def __init__(
        self,
        headers,
        pull_request,
        repository,
        review,
        sender,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.pull_request: PullRequest = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=pull_request
        )
        self.repository: Repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.review: PullRequestReview = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=review
        )
        self.sender: NamedUser = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class PullRequestReviewDismissedEvent(PullRequestReviewEvent):
    """This class represents a pull request review dismissed event."""

    event_identifier = {"action": "dismissed"}


class PullRequestReviewEditedEvent(PullRequestReviewEvent):
    """This class represents a pull request review edited event."""

    event_identifier = {"action": "edited"}

    def __init__(self, headers, changes, *args, **kwargs):
        super().__init__(headers, *args, **kwargs)
        self.changes = changes


class PullRequestReviewSubmittedEvent(PullRequestReviewEvent):
    """This class represents a pull request review submitted event."""

    event_identifier = {"action": "submitted"}

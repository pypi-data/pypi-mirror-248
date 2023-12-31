# -*- coding: UTF-8 -*-


class QantyError(Exception):
    fmt = "An unspecified error occurred"

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class InvalidUserIdentifier(QantyError):
    fmt = "Invalid user identifier: '{user_id}'"


class BranchNotFound(QantyError):
    fmt = "Branch '{branch_id}' not found"


class UserNotFound(QantyError):
    fmt = "User '{user_id}' not found"

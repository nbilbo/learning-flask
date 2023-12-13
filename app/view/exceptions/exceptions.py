class InvalidUsernamePassword(Exception):
    def __init__(self) -> None:
        super().__init__('Invalid username or password.')


class NotPostOwner(Exception):
    def __init__(self) -> None:
        super().__init__('Current user is not post owner.')

class RegisterNotFound(Exception):
    def __init__(self, register: str) -> None:
        super().__init__(f'Register {register} not found.')


class AlreadyRegistered(Exception):
    def __init__(self, register: str) -> None:
        super().__init__(f'Register {register} already exist.')


class MissingRequiredField(Exception):
    def __init__(self, field: str) -> None:
        super().__init__(f'Missing required field {field}.')

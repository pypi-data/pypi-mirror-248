class InvalidInputException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MissingEnvironmentVariable(Exception):
    def __init__(self, message):
        super().__init__(message)

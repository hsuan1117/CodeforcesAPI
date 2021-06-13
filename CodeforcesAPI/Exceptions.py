class CodeforcesException(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Salary is not in (5000, 15000) range"):
        self.message = message
        super().__init__(self.message)


class CodeforcesCredentialException(CodeforcesException):
    def __init__(self, message="Credentials provided is invalid."):
        self.message = message
        super().__init__(self.message)


class CodeforcesSessionException(CodeforcesException):
    def __init__(self, message="Session is invalid."):
        self.message = message
        super().__init__(self.message)

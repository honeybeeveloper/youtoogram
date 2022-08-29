class CustomException(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

    def to_dict(self):
        exception_result = dict()
        exception_result['error_message'] = self.error_message
        return exception_result


class PasswordLengthViolation(CustomException):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)


class UserIdLengthViolation(CustomException):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)


class DuplicatedUserId(CustomException):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)


class UserNotFound(CustomException):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)


class BadRequest(CustomException):
    def __init__(self, error_message):
        status_code = 400
        super().__init__(status_code, error_message)



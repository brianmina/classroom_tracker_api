class ClassroomTrackerException(Exception):
    def __init__(self, message: str, response_code: int = 400):
        self.message = message
        self.response_code = response_code

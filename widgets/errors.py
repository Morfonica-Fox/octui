class BaseError(Exception):
    def __init__(self, message):
        self.message = message

class OpertaionError(BaseError):
    def __init__(self, message):
        self.message = message

class DisplayError(BaseError):
    def __init__(self, message):
        self.message = message
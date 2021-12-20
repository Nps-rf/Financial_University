class IncorrectIndex(BaseException):
    """
    Happens if index incorrect
    """
    def __init__(self, message="Moved incorrect value to function, check other arguments if all are correct"):
        self.message = message
        super().__init__(self.message)


class WorkInProgress(BaseException):
    """
    Happens if part of package isn't ready
    """
    def __init__(self, message="This part is still WoIP"):
        self.message = message
        super().__init__(self.message)


class UnsupportedType(BaseException):
    """
    Happens if data type is unsupported
    """
    def __init__(self, case, message="This is unsupported type"):
        self.message = message
        self.case = case
        super().__init__(self.message.replace('This', str(case)))

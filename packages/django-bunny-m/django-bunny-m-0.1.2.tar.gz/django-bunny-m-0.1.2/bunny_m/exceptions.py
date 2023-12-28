

class ConsumerClassException(Exception):
    pass


class ConsumeException(Exception):
    pass


class NackException(ConsumeException):
    pass


class RequeueException(ConsumeException):
    pass


class EventAlreadyExistsException(Exception):
    pass

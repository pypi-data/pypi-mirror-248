class PhareError(Exception):
    pass

class DeserializeError(PhareError):
    pass

class ServerError(PhareError):
    pass

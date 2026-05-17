class DeviceManagerError(Exception):
    pass

class InvalidReferenceError(DeviceManagerError):
    pass

class NotFoundError(DeviceManagerError):
    pass

class InvalidStatusError(DeviceManagerError):
    pass
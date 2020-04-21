class BotBaseException(Exception):
    pass


class ModuleException(BotBaseException):
    pass


class ModuleNotFound(ModuleException):
    pass


class IncompatibleModuleError(ModuleException):
    pass

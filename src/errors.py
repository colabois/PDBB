class BotBaseException(Exception):
    pass


class ModuleException(BotBaseException):
    pass


class ModuleNotFoundError(ModuleException):
    pass


class IncompatibleModuleError(ModuleException):
    pass


class MissingDependency(ModuleException):
    pass

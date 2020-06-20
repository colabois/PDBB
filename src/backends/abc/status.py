import typing


class StatusType:
    ONLINE = 0
    DO_NOT_DISTURB = 1
    IDLE = 2
    INVISIBLE = 3
    OFFLINE = 4


class ActivityType:
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    CUSTOM = 4


class Activity:
    name: str
    type: ActivityType

    def __init__(self, name, activity_type):
        self.name = name
        self.type = activity_type


class Status:
    activity: Activity
    status: StatusType
    afk: bool

    def __init__(self, status, activity=None, afk=False):
        self.activity = activity
        self.status = status
        self.afk = afk

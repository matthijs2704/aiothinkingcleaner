from aiothinkingcleaner.command_base import TCCommand
from aiothinkingcleaner.data import TCEndpoint

# class TCCommand(Enum):
#     """Enum of commands available."""

#     CLEAN = "clean"
#     MAX = "max"
#     DELAYED_CLEAN = "delayedclean"
#     SPOT = "spot"
#     DOCK = "dock"
#     FIND_ME = "find_me"
#     STOP = "stop"
#     EXIT_DOCK = "leavehomebase"
#     POWER_OFF = "poweroff"
#     REBOOT = "crash"


class CLEAN(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "clean"


class MAX_CLEAN(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "max"


class DELAYED_CLEAN(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "delayedclean"


class SPOT_CLEAN(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "spot"


class DOCK(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "dock"


class FIND_ME(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "find_me"


class STOP(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "stop"


class EXIT_DOCK(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "leavehomebase"


class POWER_OFF(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "poweroff"


class REBOOT(TCCommand):
    ENDPOINT = TCEndpoint.COMMAND
    CMD = "crash"

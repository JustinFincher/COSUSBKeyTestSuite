import os
from enum import Enum
from datetime import datetime, timedelta
from Data.Test import *

class LogType(Enum):
    Info = 0
    Warning = 1
    Error = 2

class Log:
    datetime = str(datetime.now())
    message = ""
    logType = LogType.Info
    testType = TestType.COMMON_EVENT

    def stringRepresentation(self):
        return self.datetime + " " + self.testType.name + " " + self.logType.name + " " + self.message

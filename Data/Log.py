import os
from enum import Enum
from datetime import datetime, timedelta
from Data.Test import *
import time

class LogType(Enum):
    Info = 0
    Warning = 1
    Error = 2

class Log:
    datetime = None
    message = ""
    logType = LogType.Info
    testType = TestType.COMMON_EVENT

    def __init__(self):
        self.datetime = datetime.now()

    def stringRepresentation(self):
        return str(self.datetime.strftime('%Y-%m-%d-%H-%M-%S-%f')) + " " + self.testType.name + " " + self.logType.name + " " + self.message

    def getID(self):
        return self.TimestampMillisec64()

    def TimestampMillisec64(self):
        return int((self.datetime - datetime(1970, 1, 1)).total_seconds() * 1000)

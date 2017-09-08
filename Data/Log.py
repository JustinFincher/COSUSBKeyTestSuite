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
        self.datetime = time.time()

    def stringRepresentation(self):
        return datetime.fromtimestamp(self.datetime).strftime('%Y-%m-%d-%H-%M-%S') + " " + self.testType.name + " " + self.logType.name + " " + self.message

    def getID(self):
        return self.datetime


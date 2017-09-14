import os
from datetime import datetime
from Data.Log import *
import dicttoxml
from os.path import dirname, abspath
from Data.Test import TestType
from Controller.Singleton import Singleton
from Data.Test import *

class LogManager(object,metaclass=Singleton):

    logList = []
    currentLogPath = ""


    def __init__(self):
        self.newLogs()
        pass

    def newLogs(self):
        print("New Logs Inited, All List will be cleared")
        self.logList.clear()
        self.currentLogPath = self.getNewFilePath()


    def getNewFilePath(self):
        logPath = ""
        try:
            rootPath = dirname(dirname(abspath(__file__)))
            logPath = os.path.join(rootPath, 'LogsOutput',self.getNewFileName())
        except:
            print("Exception when getDLLPath()")
        finally:
            return logPath

    def getLogsPath(self):
        logsPath = ""
        try:
            rootPath = dirname(dirname(abspath(__file__)))
            logsPath = os.path.join(rootPath, 'LogsOutput')
        except:
            print("Exception when getDLLPath()")
        finally:
            return logsPath

    def getNewFileName(self):
        return str(datetime.now()).replace(" ", "-").replace(":", "-")+".xml"

    def addLog(self, newLog):
        self.logList.append(newLog)

    def addLogStr(self, message, logtype = LogType.Info, testtype = TestType.COMMON_EVENT):
        print("ADD LOG STR WITH MSG: " + message)
        log = Log()
        log.message = message
        log.logType = logtype
        log.testType = testtype
        self.logList.append(log)

    def saveLogs(self):
        listInDict = []
        for log in self.logList:
            dict = {}
            dict["message"] = log.message
            dict["datetime"] = str(log.datetime)
            dict["logType"] = str(log.logType)
            listInDict.append(dict)
        wholeDict = {"logs": listInDict}
        xml = dicttoxml.dicttoxml(wholeDict)
        print(str(xml))

        filePath = self.getNewFilePath()
        f = open(filePath, 'w')
        f.write(str(xml))
        f.close()

    def arrayRepresentation(self):
        a = []
        for log in self.logList:
            a.append(log.stringRepresentation())
        return a

    pass
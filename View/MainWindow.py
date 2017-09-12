from appJar import gui
from Controller.DeviceManager import *
import os, sys
from threading import Timer
import time
import copy
from Controller.LogManager import *
import os
import platform
import subprocess
from Controller.TestManager import *

class MainWindow:



    timer = None
    app = gui("COS USB KEY")
    logList = []


    def update(self):

        if DeviceManager().ifDLLPathExists():
            self.app.setStatusbar("动态库加载于 " + DeviceManager().getDLLPath(), 0)
        else:
            self.app.setStatusbar("动态库不存在于 " + DeviceManager().getDLLPath(), 0)

        self.app.setStatusbar("设备个数 = " + str(DeviceManager().getDeviceCount()), 1)
        # print("currentLogIDs \n")
        currentLogIDs = (o.getID() for o in self.logList)
        # print(currentLogIDs)
        # print("updatedLogIDs \n")
        updatedLogIDs = (o.getID() for o in LogManager().logList)
        # print(updatedLogIDs)
        self.logList = copy.copy(LogManager().logList)
        # print("addedLogIDs \n")
        addedLogIDs = list(set(updatedLogIDs) - set(currentLogIDs))
        # print(addedLogIDs)

        addedLogs = []
        for logID in addedLogIDs:
            logInstance = next((x for x in LogManager().logList if x.getID() == logID), None)
            if logInstance != None:
                addedLogs.append(logInstance.stringRepresentation())


        self.app.addListItems("logListBox",addedLogs)

        self.app.clearListBox("testListBox")
        self.app.addListItems("testListBox", TestManager().listOfInfo())


        self.timer = Timer(2, self.update)
        self.timer.start()




    def topMenuPress(self,name):
        if name == "REFRESH":
            self.app.setStatusbar("设备个数 = " + str(DeviceManager().getDeviceCount()), 1)
        elif name == "HELP":
            self.app.infoBox("COS TEST TOOL 帮助", "COS USB KEY 测试软件")
        elif name == "OFF":
            sys.exit()
        elif name == "SETTINGS":
            pass
        elif name == "SAVE":
            LogManager().saveLogs()
        elif name == "OPEN":
            path = LogManager().getLogsPath()
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        elif name == 'NEW':
            inputString = self.app.textBox("Input APDU","APDU HERE")
            if inputString != None:
                dict = DeviceManager().sendAPDUStr(inputString)
                print(dict)

        pass

    def runButtonPress(self,btn):
        print("runButtonPress")
        selected = self.app.getListItems("testListBox")
        print(selected)
        try:
            for name in selected:
                TestManager().runTest(name)
        except:
            pass

        pass

    def __init__(self):

        DeviceManager().loadDLL()
        self.app.setSticky("news")
        self.app.setExpand("both")

        self.app.createMenu("Connect")


        tools = ["REFRESH","OPEN" ,"SAVE", "SETTINGS", "HELP", "OFF","NEW"]

        self.app.addToolbar(tools, self.topMenuPress, findIcon=True)

        self.app.addStatusbar(fields=2)

        self.app.addLabel("infoText", "COS USB KEY 测试软件")

        self.app.setStatusbarWidth(70, 0)


        self.app.startPanedFrame("p1",)
        self.app.startLabelFrame("Tests")
        self.app.setSticky("nesw")
        self.app.addListBox("testListBox", [])
        self.app.addButton("Run", self.runButtonPress)
        self.app.stopLabelFrame()

        self.app.startPanedFrame("p2")
        self.app.startLabelFrame("Log")
        self.app.setSticky("nesw")
        self.app.addListBox("logListBox", [])
        self.app.stopLabelFrame()

        self.app.stopPanedFrame()
        self.app.stopPanedFrame()

        self.timer = Timer(2, self.update)
        self.timer.start()

        self.app.go()

    def __del__(self):
        pass




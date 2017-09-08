import os
from os.path import dirname, abspath
from Controller.Singleton import Singleton
from ctypes import *
import ctypes
import binascii
from Data.APDU import *
from Data.StatCode import *
from Controller.LogManager import *
import platform

class DeviceManager(object,metaclass=Singleton):

    dllInstance = None
    deviceCountCache = 0

    def isDLLLoaded(self):
        return self.dllInstance != None

    def __init__(self):

        pass

    def getDLLPath(self):
        dllPath = ""
        rootPath = dirname(dirname(abspath(__file__)))
        dllPath = os.path.join(rootPath, 'Library', 'usbkey.dll')
        try:
            pass
        except:
            print("Exception when getDLLPath()")
        finally:
            return dllPath

    def ifDLLPathExists(self):
        return os.path.exists(self.getDLLPath())

    def getDeviceCount(self):
        count = 0
        if self.isDLLLoaded():
            count = self.dllInstance.GetDevCount()
        else:
            count = 0

        if self.deviceCountCache != count:
            LogManager().addLog("链接设备个数为 " + str(count))
            if count > 0:
                self.deviceCountCache = count
                self.connectDeviceAll()

        self.deviceCountCache = count
        return count


    def loadDLL(self):
        if self.ifDLLPathExists():
            self.dllInstance = ctypes.WinDLL(self.getDLLPath())
            LogManager().addLog("动态库加载于 " + DeviceManager().getDLLPath())
        else:
            print("ifDLLPathExists = NO")
        pass

    def connectDevice(self,index):
        if self.isDLLLoaded():
            # print("Try connectDevice(" + str(self.dllInstance.GetDevInfo(index)) +")")
            print("Try connectDevice(" + str(index) + ")")
            # print(self.dllInstance.ConnectDevice(self.dllInstance.GetDevInfo(index)))
            if self.dllInstance.ConnectDevice(index) == 0:
                print("连接 " + str(index) + " 号设备成功")
                LogManager().addLog(("连接 " + str(index) + " 号设备成功"))

    def connectDeviceAll(self):
        if self.isDLLLoaded():
            if self.deviceCountCache >= 1:
                print("self.deviceCountCache >= 1:")
                for i in range(0,self.deviceCountCache):
                    LogManager().addLog("连接 " + str(i) + " 号设备")
                    print("self.connectDevice("+ str(i) + ")")
                    self.connectDevice(i)

    def sendAPDU(self,apdu: APDU):
        if self.isDLLLoaded():
            buffer = None
            pi = None
            self.dllInstance.TrasmitData(apdu.byteRepresentation(),apdu.getLength(),False,buffer,pi,0)

            content = buffer.raw[:pi.contents.value]
            msg = content[pi - 4:4]
            sw1 = content[pi - 2:2]
            sw2 = content[pi - 2:]

            statCode = StatCode(sw1,sw2)

            return {"msg":msg,"statCode":statCode}
        pass

    def sendAPDUStr(self, apduString):
        if self.isDLLLoaded():

            buffer = ctypes.c_buffer(64)
            pi = ctypes.c_int()

            h = bytes.fromhex(apduString)
            print(h)
            self.dllInstance.TrasmitData(h,len(h),False,buffer,ctypes.byref(pi),0)

            print(buffer)
            print(pi)
            if buffer == None or pi == None:
                return None
            else:
                content = buffer.raw[:pi.value]
                msg = content[len(content) - 4:4]
                sw1 = content[len(content) - 2:2]
                sw2 = content[len(content) - 2:]
                statCode = StatCode(sw1,sw2)
                return {"msg":msg,"statCode":statCode}
        pass

    def getDeviceInfo(self,index):
        if self.isDLLLoaded():
            print(self.dllInstance.GetDevInfo(index))
            return self.dllInstance.GetDevInfo(index)
        else:
            return 0

    pass
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
from Data.Log import *
from Data.Test import *

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
            LogManager().addLogStr("链接设备个数为 " + str(count))
            if count > 0:
                self.deviceCountCache = count
                self.connectDeviceAll()

        self.deviceCountCache = count
        return count


    def loadDLL(self):
        if self.ifDLLPathExists():
            self.dllInstance = ctypes.WinDLL(self.getDLLPath())
            LogManager().addLogStr("动态库加载于 " + DeviceManager().getDLLPath())
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
                LogManager().addLogStr(("连接 " + str(index) + " 号设备成功"))

    def connectDeviceAll(self):
        if self.isDLLLoaded():
            if self.deviceCountCache >= 1:
                print("self.deviceCountCache >= 1:")
                for i in range(0,self.deviceCountCache):
                    LogManager().addLogStr("连接 " + str(i) + " 号设备")
                    print("self.connectDevice("+ str(i) + ")")
                    self.connectDevice(i)

    def sendAPDU(self,apdu):
        print("sendAPDU")
        return self.sendAPDUStr(apdu.stringRepresentation())

    # 00 A4 00 00 02 A001 // MF
    # 00 A4 00 00 02 2001 // ADF
    # 00 A4 00 00 02 A001 // EF
    def sendAPDUStr(self, apduString):
        print("sendAPDUStr(" + apduString + ")")
        if self.isDLLLoaded():

            buffer = ctypes.create_string_buffer(512)
            i = ctypes.c_int(512)
            pi = pointer(i)

            apduString.upper().replace('0X', '')
            print("sendAPDUStr()  " + apduString)
            h = bytes.fromhex(apduString)
            # print("Hex = " + str(h))
            self.dllInstance.TrasmitData(h, c_int(len(h)), c_bool(False), buffer, pi, c_int(0))

            print("buffer = " + str(buffer.raw))
            print("pi.contents.value = " + str(pi.contents.value))
            if buffer == None or pi == None:
                print("buffer == None or pi == None:")
                return None
            else:
                bytesStr = buffer.raw[:pi.contents.value]
                print("bytesStr = " + str(bytesStr))
                content = str(binascii.hexlify(bytesStr).decode('utf8'))
                print("Content = " + str(content) + " Length = " + str(len(content)))
                if len(content) >= 4:
                    msg = content[:len(content) - 4]
                    sw1 = content[len(content)-4:-2]
                    sw2 = content[-2:]
                    statCode = StatCode(sw1,sw2)
                    print("msg = " + str(msg) + " sw1 = " + str(sw1) + " sw2 = " + str(sw2))
                    return {"msg":msg,"statCode":statCode}
        else:
            print("ERR self.isDLLLoaded() = FALSE")
            LogManager().addLogStr("DLL is not Loaded", LogType.Error, TestType.COMMON_EVENT)
        return None

    def getDeviceInfo(self,index):
        if self.isDLLLoaded():
            print(self.dllInstance.GetDevInfo(index))
            return self.dllInstance.GetDevInfo(index)
        else:
            return 0

    pass
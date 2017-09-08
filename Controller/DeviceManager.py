import os
from os.path import dirname, abspath
from Controller.Singleton import Singleton
from ctypes import *
import ctypes
import binascii
from Data.APDU import *
import platform

class DeviceManager(object,metaclass=Singleton):

    dllInstance = None

    def isDLLLoaded(self):
        return self.dllInstance != None

    def __init__(self):
        self.loadDLL()
        pass

    def getDLLPath(self):
        dllPath = ""
        try:
            rootPath = dirname(dirname(abspath(__file__)))
            dllPath = os.path.join(rootPath, 'Library', 'usbkey.dll')
        except:
            print("Exception when getDLLPath()")
        finally:
            return dllPath

    def ifDLLPathExists(self):
        return os.path.exists(self.getDLLPath())

    def getDeviceCount(self):
        if self.isDLLLoaded():
            return self.dllInstance.GetDevCount()
        else:
            return 0

    def loadDLL(self):
        try:
            if self.ifDLLPathExists():
                self.dllInstance = ctypes.WinDLL(self.getDLLPath())
            else:
                print("ifDLLPathExists = NO")
            pass
        except:
            print("Load DLL Error")
        finally:
            pass

    def connectDevice(self,index):
        if self.isDLLLoaded():
            self.dllInstance.ConnectDevice(index)

    def connectDeviceAll(self):
        if self.isDLLLoaded():
            if self.getDeviceCount() > 1:
                for i in range(0,self.getDeviceCount() - 1):
                    self.connectDevice(i)

    def sendAPDU(self,apdu: APDU):
        if self.isDLLLoaded():
            buffer = None
            pi = None
            self.dllInstance.TrasmitData(apdu.byteRepresentation(),apdu.getLength(),False,buffer,pi,0)

            # get StatCode Here
        pass

    def getDeviceInfo(self):
        if self.isDLLLoaded():
            self.dllInstance.GetDevInfo()

    pass
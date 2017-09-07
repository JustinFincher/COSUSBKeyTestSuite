import os
from os.path import dirname, abspath
from Controller.Singleton import Singleton
from ctypes import *
import ctypes
import binascii
import platform

class DeviceManager(object,metaclass=Singleton):

    dllInstance = None

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
        if self.dllInstance != None:
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


    pass
import os
from enum import Enum
from Controller.DeviceManager import *

class TestType(Enum):
    NON_DEFINED = 0
    TEST_SELECT_FILE = 1
    TEST_BINARY_READ = 2
    TEST_BINARY_WRITE = 3
    TEST_INIT = 4
    TEST_VALIDATE_PIN = 5
    TEST_CHANGE_PIN = 6
    TEST_READ_PUB_KEY = 7
    TEST_GEN_PAR = 8
    TEST_RSA_LOCK_UNLOCK = 9
    TEST_RSA_SIGN = 10
    TEST_RANDOM_NUM = 11
    COMMON_EVENT = 12


class Test:

    def run(self):
        print("Test Will Run")
        return True

    @staticmethod
    def getInfo():
        return "Test Base Class"

    @staticmethod
    def getTestType():
        return TestType.NON_DEFINED

    def getSelectFileBool(self,pos):
        from Controller.Helper import Helper
        from Controller.LogManager import LogManager

        LogManager().addLogStr("getSelectFileBool " + str(pos))

        res = False
        try:
            dict = Helper().getSelectFileDict(pos)
            if (dict != None) and ('statCode' in dict):
                print(dict)
                statCode = dict["statCode"].statCode
                if statCode == StatCodeType.STAT_CODE_SUCCESS:
                    res = True
        except:
            pass
        finally:
            print("getSelectFileBool " + str(pos) + "YES" if res else "NO")
            return res
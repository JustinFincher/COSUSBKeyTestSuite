from Data.Test import *
from Controller.DeviceManager import *
from Controller.Helper import *

class TEST_SELECT_FILE(Test):

    def run(self):
        superResult = super().run()
        print("TEST_SELECT_FILE run()")
        res = True

        testResList = []
        testResList.append(self.getSelectFileBool(FileLocationType.MF))
        testResList.append(self.getSelectFileBool(FileLocationType.ADF))
        testResList.append(self.getSelectFileBool(FileLocationType.IKF))

        for isSuccessful in testResList:
            res = res and isSuccessful

        return res

    @staticmethod
    def getInfo():
        return "测试选择文件"

    @staticmethod
    def getTestType():
        return TestType.TEST_SELECT_FILE


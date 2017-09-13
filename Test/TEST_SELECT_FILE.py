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

        testResList.append(self.getSelectFileBool(FileLocationType.MF))
        testResList.append(self.getSelectFileBool(FileLocationType.GPKF))

        testResList.append(self.getSelectFileBool(FileLocationType.MF))
        testResList.append(self.getSelectFileBool(FileLocationType.EFTokenInfo))

        testResList.append(self.getSelectFileBool(FileLocationType.MF))
        testResList.append(self.getSelectFileBool(FileLocationType.EFPublic))

        testResList.append(self.getSelectFileBool(FileLocationType.MF))
        testResList.append(self.getSelectFileBool(FileLocationType.EFPrivate))

        for isSuccessful in testResList:
            res = res and isSuccessful

        return res

    @staticmethod
    def getInfo():
        return "测试选择文件"

    @staticmethod
    def getTestType():
        return TestType.TEST_SELECT_FILE

    def getSelectFileBool(self,pos):
        LogManager().addLog("getSelectFileBool " + str(pos))
        print("getSelectFileBool " + str(pos))

        res = False
        try:
            dict = Helper().getSelectFileDict(pos)
            if (dict != None) and ('statCode' in dict):
                statCode = dict["statCode"]
                if statCode == StatCodeType.STAT_CODE_SUCCESS:
                    res = True
        except:
            print("Bug")
            pass
        finally:
            return res

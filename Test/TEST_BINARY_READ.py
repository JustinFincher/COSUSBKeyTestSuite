from Data.Test import *
from Controller.Helper import *

class TEST_BINARY_READ(Test):

    def run(self):
        superResult = super().run()

        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        dict = Helper().getSelectFileDict(FileLocationType.EFTokenInfo)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False
            print(dict["msg"])

        dict = Helper.getBinaryReadDict()
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False
            print(dict["msg"])


        return True

    @staticmethod
    def getInfo():
        return "测试二进制读"

    @staticmethod
    def getTestType():
        return TestType.TEST_BINARY_READ
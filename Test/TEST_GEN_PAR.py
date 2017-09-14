from Data.Test import *
from Data.StatCode import *
from Controller.Helper import *

class TEST_GEN_PAR(Test):

    def run(self):
        superResult = super().run()

        # SELECT MF
        res = False
        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                res = True

        # VALIDATE PIN
        if res == True:
            pass

        # GEN PAR

        return res

    @staticmethod
    def getInfo():
        return "测试生成密钥对"

    @staticmethod
    def getTestType():
        return TestType.TEST_GEN_PAR
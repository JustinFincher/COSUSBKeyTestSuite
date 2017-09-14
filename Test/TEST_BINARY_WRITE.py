from Data.Test import *
from Controller.Helper import *

class TEST_BINARY_WRITE(Test):

    def run(self):
        superResult = super().run()

        hexToWrite = "00D60000"
        # hexToWrite = "11111111"

        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("NAVIGATE TO MF",LogType.Info,self.getTestType())

        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("NAVIGATE TO ADF", LogType.Info, self.getTestType())

        dict = Helper().getSelectFileDict(FileLocationType.EFTokenInfo)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("NAVIGATE TO EF TOKEN INFO", LogType.Info, self.getTestType())

        dict = Helper().getBinaryReadDict("00","00","08")
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("READ MSG = " + str(dict["msg"]), LogType.Info, self.getTestType())

        dict = Helper().getBinaryWriteDict("00","00",hexToWrite)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("WRITE 0000 to " + str(hexToWrite) + " Res = " + str(dict["msg"]), LogType.Info, self.getTestType())

        dict = Helper().getBinaryReadDict("00", "00", "04")
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("READ MSG AGAIN = " + str(dict["msg"]), LogType.Info, self.getTestType())

        if str(hexToWrite) == str(dict["msg"]).upper():
            LogManager().addLogStr("HEX R/W EQUAL", LogType.Info, self.getTestType())
            return True
        else:
            LogManager().addLogStr("HEX R/W NOT EQUAL", LogType.Error, self.getTestType())
            return True

    @staticmethod
    def getInfo():
        return "测试二进制写"

    @staticmethod
    def getTestType():
        return TestType.TEST_BINARY_WRITE
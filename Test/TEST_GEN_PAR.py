from Data.Test import *
from Data.StatCode import *
import pyDes
from Controller.Helper import *

class TEST_GEN_PAR(Test):

    def run(self):
        superResult = super().run()

        from Data.Log import LogType

        # SELECT MF
        LogManager().addLogStr("WILL SELECT MF",LogType.Info,self.getTestType())
        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        # SELECT ADF
        LogManager().addLogStr("WILL SELECT ADF", LogType.Info, self.getTestType())
        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False



        # VALIDATE PIN
        LogManager().addLogStr("WILL VALIDATE PIN", LogType.Info, self.getTestType())
        pin = "1234"
        hexifiedPin = Helper().getMd5HashHex(pin)
        print(hexifiedPin)
        hexifiedPin = Helper().replaceFFWithFE(hexifiedPin)
        print(hexifiedPin)

        randomMsg = Helper().getChallengeMsg()
        print("RANDOM MSG = " + str(randomMsg))
        if randomMsg == None:
            print("TEST_VALIDATE_PIN FALSE")
            return False

        mfRes = self.getSelectFileBool(FileLocationType.MF)
        adfRes = self.getSelectFileBool(FileLocationType.ADF)

        print(mfRes)
        print(adfRes)

        bytesRandom = bytes.fromhex(randomMsg)
        print("ByteRandom = " + str(bytesRandom))
        print("bytes.fromhex(hexifiedPin) = " + str(bytes.fromhex(hexifiedPin)))
        pyDesInstance = pyDes.triple_des(bytes.fromhex(hexifiedPin), pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None,
                                         padmode=pyDes.PAD_NORMAL)
        print("pyDesInstance = " + str(pyDesInstance))
        pyRes = pyDesInstance.encrypt(bytesRandom)
        print("pyRes = " + str(pyRes))
        print("pyRes.hex() = " + str(pyRes.hex()))
        resDict = Helper().getVerifyPinDict(pyRes.hex())
        if resDict["statCode"].statCode != StatCodeType.STAT_CODE_SUCCESS:
            return False

        # MSE
        LogManager().addLogStr("WILL SET UP MSE", LogType.Info, self.getTestType())
        dict = Helper().getMSEGenParDict("01", "22", 4)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        # GEN PAR
        LogManager().addLogStr("WILL GEN PAIR", LogType.Info, self.getTestType())
        dict = Helper().getGenKeyPairDict()
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        return True

    @staticmethod
    def getInfo():
        return "测试生成密钥对"

    @staticmethod
    def getTestType():
        return TestType.TEST_GEN_PAR
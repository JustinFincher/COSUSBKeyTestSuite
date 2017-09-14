from Data.Test import *
from Data.StatCode import *
import pyDes
from Controller.Helper import *

class TEST_GEN_PAR(Test):

    def run(self):
        superResult = super().run()

        # SELECT MF
        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        # VALIDATE PIN

        pin = "1234"
        hexifiedPin = Helper().getMd5HashHex(pin)
        print(hexifiedPin)
        hexifiedPin.upper().replace("FF", "FE")
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
        dict = Helper().getMSEGenParDict("00", "22")
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        # GEN PAR
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
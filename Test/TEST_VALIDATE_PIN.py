from Data.Test import *
from Controller.Helper import *
import pyDes

class TEST_VALIDATE_PIN(Test):

    def run(self):
        superResult = super().run()

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

        bytesRandom = bytes.fromhex(randomMsg)
        print("ByteRandom = " + str(bytesRandom))
        print("bytes.fromhex(hexifiedPin) = " + str(bytes.fromhex(hexifiedPin)))
        pyDesInstance = pyDes.triple_des(bytes.fromhex(hexifiedPin), pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        print("pyDesInstance = " + str(pyDesInstance))
        pyRes = pyDesInstance.encrypt(bytesRandom)
        print("pyRes = " + str(pyRes))
        print("pyRes.hex() = " + str(pyRes.hex()))
        resDict = Helper().getVerifyPinDict(pyRes.hex())
        if resDict["statCode"].statCode == StatCodeType.STAT_CODE_SUCCESS:
            print("TEST_VALIDATE_PIN TRUE")
            return True
        else:
            print("TEST_VALIDATE_PIN FALSE")
            return False


    @staticmethod
    def getInfo():
        return "测试验证 PIN"

    @staticmethod
    def getTestType():
        return TestType.TEST_VALIDATE_PIN
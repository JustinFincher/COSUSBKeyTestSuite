from Data.Test import *
from Controller.Helper import *
import pyDes

class TEST_VALIDATE_PIN(Test):

    def run(self):
        superResult = super().run()

        pin = "1234"
        hexifiedPin = Helper().getMd5HashHex(pin)
        print(hexifiedPin)
        hexifiedPin.upper().replace("FF","FE")
        print(hexifiedPin)

        randomMsg = Helper().getChallengeMsg()
        print(randomMsg)
        if randomMsg == None:
            print("TEST_VALIDATE_PIN FALSE")
            return False

        pyDesInstance = pyDes.triple_des(bytes.fromhex(hexifiedPin), pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        print("pyDesInstance = " + str(pyDesInstance))
        pyRes = pyDesInstance.encrypt(randomMsg)
        print("pyRes = " + str(pyRes))
        Helper().getVerifyPinDict(pyRes)

        print("TEST_VALIDATE_PIN TRUE")
        return True

    @staticmethod
    def getInfo():
        return "测试 PIN"

    @staticmethod
    def getTestType():
        return TestType.TEST_VALIDATE_PIN
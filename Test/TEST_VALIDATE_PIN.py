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

        mfRes = self.getSelectFileBool(FileLocationType.MF)
        adfRes = self.getSelectFileBool(FileLocationType.ADF)

        pyDesInstance = pyDes.triple_des(bytes.fromhex(hexifiedPin), pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_NORMAL)
        print("pyDesInstance = " + str(pyDesInstance))
        pyRes = pyDesInstance.encrypt(randomMsg)
        print("pyRes = " + str(pyRes))
        print("pyRes.hex() = " + str(pyRes.hex()))
        resDict = Helper().getVerifyPinDict(pyRes.hex())
        if resDict["statCode"] == StatCodeType.STAT_CODE_SUCCESS:
            print("TEST_VALIDATE_PIN TRUE")
            return True
        else:
            print("TEST_VALIDATE_PIN FALSE")
            return False


    @staticmethod
    def getInfo():
        return "测试 PIN"

    @staticmethod
    def getTestType():
        return TestType.TEST_VALIDATE_PIN

    def getSelectFileBool(self,pos):
        LogManager().addLogStr("getSelectFileBool " + str(pos))
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
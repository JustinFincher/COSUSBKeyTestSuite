from Data.Test import *

class TEST_RSA_SIGN(Test):

    def run(self):
        superResult = super().run()
        return True

    @staticmethod
    def getInfo():
        return "测试 RSA 签名"

    @staticmethod
    def getTestType():
        return TestType.TEST_RSA_SIGN
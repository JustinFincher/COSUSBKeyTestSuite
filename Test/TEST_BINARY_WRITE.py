from Data.Test import *

class TEST_BINARY_WRITE(Test):

    def run(self):
        superResult = super().run()

        stuffToWrite = "00000000"

        return True

    @staticmethod
    def getInfo():
        return "测试二进制写"

    @staticmethod
    def getTestType():
        return TestType.TEST_BINARY_WRITE
from Data.Test import *

class TEST_INIT(Test):

    @staticmethod
    def run():
        return True

    @staticmethod
    def getInfo():
        return "测试初始化"

    @staticmethod
    def getTestType():
        return TestType.TEST_INIT
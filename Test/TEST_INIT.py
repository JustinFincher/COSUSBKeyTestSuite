from Data.Test import *

class TEST_INIT(Test):

    def run(self):
        superResult = super().run()
        return True

    @staticmethod
    def getInfo():
        return "测试初始化"

    @staticmethod
    def getTestType():
        return TestType.TEST_INIT
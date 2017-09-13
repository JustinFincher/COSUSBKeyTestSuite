from Data.Test import *
from Controller.Helper import *
from Controller.DeviceManager import *
from Data.StatCode import *

class TEST_RANDOM_NUM(Test):

    def run(self):
        superResult = super().run()

        randomMsg = Helper().getChallengeMsg()
        print(randomMsg)
        if randomMsg == None:
            print("TEST_RANDOM_NUM FALSE")
            return False

        return True

    @staticmethod
    def getInfo():
        return "测试随机数生成"

    @staticmethod
    def getTestType():
        return TestType.TEST_RANDOM_NUM
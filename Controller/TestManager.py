from Controller.Singleton import Singleton
from os.path import dirname, abspath
from Data.Test import *
import os
from Test import *
from Controller.LogManager import *

class TestManager(object,metaclass=Singleton):


    testClassesList = []


    def __init__(self):
        self.refreshList()
        pass

    def refreshList(self):
        self.testClassesList.clear()
        classes = self.getALlTestSubClasses()
        for cls in classes:
            dict = {"Info": cls.getInfo(), "TestType": cls.getTestType(), "Class": cls}
            self.testClassesList.append(dict)
        print(self.testClassesList)

    def listOfInfo(self):
        return [x['Info'] for x in self.testClassesList]


    def getTestPyFolderPath(self):
        testPath = ""
        try:
            rootPath = dirname(dirname(abspath(__file__)))
            testPath = os.path.join(rootPath, 'Test')
        except:
            print("Exception when getTestPyFolderPath()")
        finally:
            return testPath


    def getALlTestSubClasses(self):
        testSubClasses = self.get_all_subclasses(Test)
        return testSubClasses

    # CAN USED TO FIND SUBCLASS OF SUBCLASS
    def get_all_subclasses(self,cls):
        all_subclasses = []

        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            # all_subclasses.extend(TestManager().get_all_subclasses(subclass))

        return all_subclasses

    def runTest(self,name):
        from Data.Log import LogType

        LogManager().addLogStr("Will Run Test " + str(name))
        print("runTest -> " + name)
        for test in self.testClassesList:
            if test["Info"] == name:
                print("test.getInfo() == name:")
                result = test["Class"]().run()
                LogManager().addLogStr("Test Run Finished With Result = " + str(result),LogType.Info,test["Class"].getTestType())
                print("Test Run Finished With Result = "+str(result))

    pass
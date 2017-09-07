from Controller.Singleton import Singleton
from os.path import dirname, abspath
import os

class TestManager(object,metaclass=Singleton):

    def getTestPyFolderPath(self):
        testPath = ""
        try:
            rootPath = dirname(dirname(abspath(__file__)))
            testPath = os.path.join(rootPath, 'Test')
        except:
            print("Exception when getTestPyFolderPath()")
        finally:
            return testPath



    pass
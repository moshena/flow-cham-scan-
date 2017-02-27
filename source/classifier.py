import numpy as np
import HEADER


class classifier:

    imagelists = None
    image = None
    cursorX = None
    cursorY = None

    def __init__(self,image):
        self.image = image
        self.cursorX = 0
        self.cursorY = 0

    def startProcess(self):# this funcation will manage the others one and return status to the caller
        return HEADER.unimplement

    def ObjectSpliter(self):#here we will get image and split here to shapes +open object to save location and more
        pass

    def StartRecognize(self,subimage):#from here we will start wo recognize each shape image
        pass

    def Recognizer(self,image):#process engine
        pass



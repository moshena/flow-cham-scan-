import numpy as np
import cv2
from matplotlib import pyplot as plt


class classifier:

    imagelists = None
    image = None
    def __init__(self,image):
        self.image = image

    def startProcess(self):# this funcation will manage the others one and return status to the caller
        pass

    def imageVerifier(self):# here we will check the image
        pass

    def ObjectSpliter(self):#here we will get image and split here to shapes +open object to save location and more
        pass

    def StartRecognize(self):#from here we will start wo recognize each shape image
        pass

    def Recognizer(self,image):#process engine
        pass


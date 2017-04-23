import HEADER
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage

class classifier:

    imagelists = None
    image = None
    imageFilter = None
    cursorX = None
    cursorY = None

    def __init__(self):
        self.image = None
        self.cursorX = 0
        self.cursorY = 0

    def startProcess(self,data):# this funcation will manage the others one and return status to the caller
        self.image = data.image
        self.imageFilter = data.filteredImg

        self.ObjectSpliter()
        return HEADER.unimplement

    def ObjectSpliter(self):#here we will get image and split here to shapes +open object to save location and more
        x3 = 0
        x4 = 0
        img = self.image
        col2 = self.imageFilter
        col = Image.fromarray(self.imageFilter)
        gray = col.convert('L')

        bw = np.asarray(gray).copy()

        im_med = ndimage.median_filter(bw, 25)
        new_im = np.abs(im_med)

        # here we will try to recognize shapes
        x = -1
        y = -1
        xsize, ysize = new_im.shape
        for y in range(0, ysize - 1):
            for x in range(0, xsize - 1):
                if (new_im[x][y] == 255):

                    h = 1;
                    maxX = x
                    minX = x
                    maxY = y
                    minY = y
                    tempx = x
                    tempy = y
                    stack = set(((tempx, tempy),))
                    fill_value = 50
                    orig_value = 255

                    while stack:
                        x1, y1 = stack.pop()

                        if new_im[x1, y1] == orig_value:

                            if (x1 > maxX):
                                maxX = x1

                            if (x1 < minX):
                                minX = x1

                            if (y1 > maxY):
                                maxY = y1

                            if (y1 < minY):
                                minY = y1

                            new_im[maxX, maxY] = 170
                            new_im[minX, minY] = 170
                            new_im[x1, y1] = fill_value

                            if x1 > 0:
                                stack.add((x1 - 1, y1))
                            if x1 < (xsize - 2):
                                stack.add((x1 + 1, y1))
                            if y1 > 0:
                                stack.add((x1, y1 - 1))
                            if y1 < (ysize - 2):
                                stack.add((x1, y1 + 1))

                    imfile = Image.fromarray(new_im)

                    if (maxX - minX < 1 or maxY - minY < 1):
                        pass
                    elif (maxX < xsize and maxY < ysize):

                        crop_img = col2[minX:maxX, minY: maxY]

                        imfile = Image.fromarray(crop_img)

                        x4 = x4 + 1
                        imfile.save("objecte" + str(x4) + ".png")

                    else:
                        print("out of range - x,y " + str(maxX) + "," + str(maxY))

    def StartRecognize(self,subimage):#from here we will start wo recognize each shape image
        pass

    def Recognizer(self,image):#process engine
        pass



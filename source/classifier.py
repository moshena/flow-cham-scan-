import HEADER
from PIL import Image
import numpy as np
import cv2
from datetime import datetime
import objects
from matplotlib import pyplot as plt
from scipy import ndimage
import tensorflow as tf, sys
import os



CONST_COLOR_WHITE = 255
CONST_COLOR_BLACK = 0
CONST_COLOR_VOID = 2
CONST_COLOR_RECO = 200
CONST_COLOR_UNKOWN = 3
CONST_COLOR_SEARCH = 244
CONST_COLOR_LIMIT1 = 20
CONST_COLOR_LIMIT2 = 21

CONST_YLINE = 1
CONST_XLINE = 2
CONST_BOTH_XYLINES = 3


CONST_SIZE_LINE = 30



class classifier:

    imagelists = None
    image = None
    imageFilter = None
    firstCall = True
    image_data = None
    STATIC_ID = 0
    def __init__(self):
        self.image = None
        self.data = None

        self.objectList = []

    def startProcess(self,data):# this funcation will manage the others one and return status to the caller
        self.image = data.image
        self.imageFilter = data.filteredImg
        self.data = data

        self.ObjectSpliter()
        return HEADER.unimplement

    def ObjectSpliter(self):#here we will get image and split here to shapes +open object to save location and more
        now1 = datetime.now()
        col = Image.fromarray(self.imageFilter)
        gray = col.convert('L')

        bw = np.asarray(gray).copy()
        a = np.zeros_like(bw)
        im_without_void = np.zeros_like(bw)
        im_without_void[im_without_void==0] = 255
        # here we will try to recognize shapes

        bw[bw> 150] = 255
        bw [bw< 150] = 0

        new_im = bw.copy()

        ZERO_LIMIT_Y = 0
        ZERO_LIMIT_X = 0
        xsize, ysize = new_im.shape

        for y in range(ZERO_LIMIT_Y, ysize - 1):
            for x in range(ZERO_LIMIT_X, xsize - 1):
                if (new_im[x][y] == CONST_COLOR_BLACK):

                    maxX = x
                    minX = x
                    maxY = y
                    minY = y
                    tempx = x
                    tempy = y
                    stack = set(((tempx, tempy),))

                    sum=0
                    while stack:
                        sum = sum+1
                        x1, y1 = stack.pop()

                        if new_im[x1, y1] ==  CONST_COLOR_BLACK :

                            if (x1 > maxX):
                                maxX = x1

                            if (x1 < minX):
                                minX = x1

                            if (y1 > maxY):
                                maxY = y1

                            if (y1 < minY):
                                minY = y1

                            new_im[x1, y1] = CONST_COLOR_SEARCH
                            a[x1,y1] = CONST_COLOR_WHITE

                            if x1 > ZERO_LIMIT_X:
                                stack.add((x1 - 1, y1))
                            if x1 < (xsize - 2):
                                stack.add((x1 + 1, y1))
                            if y1 > ZERO_LIMIT_Y:
                                stack.add((x1, y1 - 1))
                            if y1 < (ysize - 2):
                                stack.add((x1, y1 + 1))

                    if (maxX - minX < 1 or maxY - minY < 1):
                        pass
                    elif (maxX < xsize and maxY < ysize):
                        if (minX - 20 > ZERO_LIMIT_X):
                            minX = minX - 20

                        if (minY - 20 > ZERO_LIMIT_Y):
                            minY = minY - 20

                        if (maxX + 20 < xsize-1):
                            maxX = maxX + 20

                        if (maxY + 20 < ysize-1):
                            maxY = maxY + 20

                        now = datetime.now()
                        string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]
                        crop_img = a[minX:maxX, minY: maxY]

                        if(sum >100):
                            cv2.imwrite("object.jpeg", crop_img)
                            strResult = self.Recognizer(crop_img, (int)((minY + maxY) / 2), (int)((minX + maxX) / 2))
                            if(strResult=="void" and sum >200):
                                im_without_void=im_without_void-a
                            print(strResult)
                            a = np.zeros_like(bw)

                            points=[]
                            points.append(objects.Point(tempx,tempy))

                            color_to_draw = -1

                            if(strResult == "void"):
                                new_im[new_im == CONST_COLOR_SEARCH] = color_to_draw
                            else:
                                new_im[new_im == CONST_COLOR_SEARCH] = CONST_COLOR_WHITE


        cv2.imwrite("trash/object.jpeg", new_im)
        cv2.imwrite("trash/image.jpeg",self.data.bwImage)
        cv2.imwrite("trash/clear_lines.png", im_without_void)
        cv2.imwrite("trash/BW.png", self.data.bwImage)

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NEW~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        bw = im_without_void

        im_med = ndimage.median_filter(bw, 49)

        kernel = np.ones((13, 13), np.float32) /13*13
        dst = cv2.filter2D(im_med, -1, kernel)

        dst[dst < 1] = 0
        dst[dst >= 1] = 255

        dst = dst & bw
        shapes = dst

        dst[dst < 150] = 0
        dst[dst >= 150] = 255


        dst = bw-dst

        im_med = ndimage.median_filter(dst, 49)

        ZERO_LIMIT_Y = 0
        ZERO_LIMIT_X = 0
        xsize, ysize = shapes.shape
        for y in range(ZERO_LIMIT_Y, ysize - 1):
            for x in range(ZERO_LIMIT_X, xsize - 1):
                if (shapes[x][y] == CONST_COLOR_WHITE):

                    maxX = x
                    minX = x
                    maxY = y
                    minY = y
                    tempx = x
                    tempy = y
                    stack = set(((tempx, tempy),))

                    sum = 0
                    while stack:
                        sum = sum + 1
                        x1, y1 = stack.pop()

                        if shapes[x1, y1] == CONST_COLOR_WHITE:

                            if (x1 > maxX):
                                maxX = x1

                            if (x1 < minX):
                                minX = x1

                            if (y1 > maxY):
                                maxY = y1

                            if (y1 < minY):
                                minY = y1

                            shapes[x1, y1] = CONST_COLOR_SEARCH

                            if x1 > ZERO_LIMIT_X:
                                stack.add((x1 - 1, y1))
                            if x1 < (xsize - 2):
                                stack.add((x1 + 1, y1))
                            if y1 > ZERO_LIMIT_Y:
                                stack.add((x1, y1 - 1))
                            if y1 < (ysize - 2):
                                stack.add((x1, y1 + 1))

                    if (maxX - minX < 1 or maxY - minY < 1):
                        pass
                    elif (maxX < xsize and maxY < ysize):
                        if (minX - 20 > ZERO_LIMIT_X):
                            minX = minX - 20

                        if (minY - 20 > ZERO_LIMIT_Y):
                            minY = minY - 20

                        if (maxX + 20 < xsize - 1):
                            maxX = maxX + 20

                        if (maxY + 20 < ysize - 1):
                            maxY = maxY + 20

                        now = datetime.now()
                        string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]
                        crop_img = shapes[minX:maxX, minY: maxY]

                        if (sum > 3000):
                            print(sum)
                            cv2.imwrite("object.jpeg", crop_img)
                            strResult = self.Recognizer(crop_img, (int)((minY + maxY) / 2), (int)((minX + maxX) / 2))

                            print(strResult)

                            now = datetime.now()

                            string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]

                            # cv2.imwrite(string_i_want + strResult+"object.jpeg", crop_img)

                            points = []
                            points.append(objects.Point(tempx, tempy))

                            color_to_draw = -1
                            if (strResult == "gar"):
                                color_to_draw = CONST_COLOR_UNKOWN
                            elif (strResult == "void"):
                                color_to_draw = CONST_COLOR_VOID
                            elif (strResult == "rec"):
                                color_to_draw = CONST_COLOR_RECO
                                rec = objects.Rectangle(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY, points)
                                self.objectList.append(rec)
                            elif (strResult == "rho"):
                                color_to_draw = CONST_COLOR_RECO
                                rho = objects.Rhombus(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY, points)
                                self.objectList.append(rho)
                            elif (strResult == "square"):
                                color_to_draw = CONST_COLOR_RECO
                                s = objects.Square(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY, points)
                                self.objectList.append(s)
                            elif (strResult == "circle"):
                                color_to_draw = CONST_COLOR_RECO
                                c = objects.Circle(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY, points)
                                self.objectList.append(c)

                            if (color_to_draw != CONST_COLOR_VOID and color_to_draw != CONST_COLOR_UNKOWN):
                                self.STATIC_ID = self.STATIC_ID + 1
                            elif(color_to_draw == CONST_COLOR_UNKOWN):
                                shapes[shapes == CONST_COLOR_SEARCH] = 0
                                color_to_draw = CONST_COLOR_RECO

                            shapes[shapes == CONST_COLOR_SEARCH] = self.STATIC_ID -1 +100
                        else:
                            shapes[shapes == CONST_COLOR_SEARCH] = 0

        cv2.imwrite("shapesFirstloop.jpeg", shapes)


        copmpleteImg = bw.copy()
        copmpleteImg[shapes>100] = 0
        fullImage = copmpleteImg + shapes

        cv2.imwrite("fullimage.jpeg", fullImage)
        fullImage[fullImage>200] = 255#clean changes
        fullImage[fullImage < 100] = 0

        # in this loop we trying to arrive from White area to area that in range 100,200
        # WHITE area - Vectors+ gar
        # range 100,200 known shapes with ID in (ID = value -100)
        for y in range(ZERO_LIMIT_Y, ysize - 1):
            for x in range(ZERO_LIMIT_X, xsize - 1):
                if (fullImage[x][y] == CONST_COLOR_WHITE):

                    maxX = x
                    minX = x
                    maxY = y
                    minY = y
                    tempx = x
                    tempy = y
                    stack = set(((tempx, tempy),))
                    adjList = []

                    sum = 0
                    while stack:
                        sum = sum + 1
                        x1, y1 = stack.pop()

                        if fullImage[x1, y1] == CONST_COLOR_WHITE:

                            if (x1 > maxX):
                                maxX = x1

                            if (x1 < minX):
                                minX = x1

                            if (y1 > maxY):
                                maxY = y1

                            if (y1 < minY):
                                minY = y1

                            fullImage[x1, y1] = 15

                            if x1 > ZERO_LIMIT_X:
                                stack.add((x1 - 1, y1))
                            if x1 < (xsize - 2):
                                stack.add((x1 + 1, y1))
                            if y1 > ZERO_LIMIT_Y:
                                stack.add((x1, y1 - 1))
                            if y1 < (ysize - 2):
                                stack.add((x1, y1 + 1))

                        elif(shapes[x1, y1] in range(100,200)):
                            id = shapes[x1][y1]-100
                            FLAGExist = False
                            for adj in adjList:
                                if adj == id:
                                    FLAGExist = True
                            if(FLAGExist == False):
                                adjList.append(id)
                    if(sum > 100 and len(adjList) > 1):
                        crop_img = bw[minX:maxX, minY: maxY]
                        cv2.imwrite(str(adjList) + "vector.jpeg", crop_img)

                        print(adjList)

                    cv2.imwrite("fullimageEnd.jpeg", fullImage)
        now2 = datetime.now()
        print(now2-now1)
    def Recognizer(self,image , xWrite , yWrite):#process engine
        # init data
        # 1. image 2.labels 3.graph
        string  = ""
        image_path = "object.jpeg"

        # Read in the image_data
        self.image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        if(self.firstCall):
            self.firstCall = False
            # Loads label file, strips off carriage return
            self.label_lines = [line.rstrip() for line
                           in tf.gfile.GFile("retrained_labels.txt")]

            # Unpersists graph from file
            with tf.gfile.FastGFile('output_graph.pb', 'rb') as f:
                self.graph_def = tf.GraphDef()
                self.graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(self.graph_def, name='')


        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': self.image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            flagFirst =  True
            for node_id in top_k:
                human_string = self.label_lines[node_id]
                score = predictions[0][node_id]
                #print('%s (score = %.5f)' % (human_string, score))
                if(flagFirst):
                    string = human_string
                    flagFirst = False

        font = cv2.FONT_HERSHEY_SIMPLEX
        if(string != "gar"):
            cv2.putText(self.data.bwImage, string, (xWrite, yWrite), font, 1, (0, 255, 0), 2, cv2.LINE_8)

        return string

    def IsInLine(self,imageArray,x,y):

        left =right =up =down = True

        for i in range(x-CONST_SIZE_LINE,x+CONST_SIZE_LINE):
            if i >= self.sizeX:
                break
            elif i<0 :
                pass
            elif imageArray[i,y] != CONST_COLOR_WHITE:
                if(i<x):
                    left = False
                else:
                    right = False

        for i in range(y-CONST_SIZE_LINE,y+CONST_SIZE_LINE):
            if i >= self.sizeY:
                break
            elif i<0 :
                pass
            if imageArray[x,i] != CONST_COLOR_WHITE:
                if(i<y):
                    down = False
                else:
                    up = False


        if up == False and down == False and left == False and right == False:
            return CONST_BOTH_XYLINES
        elif up == False and down == False:
            return CONST_YLINE
        elif left == False and right == False:
            return CONST_XLINE
        else:
            return 0

    def IsInLimit(self,imageArray,x,y):

        if imageArray[x][y] !=CONST_COLOR_WHITE:
            return False

        if imageArray[x][y-1] == CONST_COLOR_WHITE and imageArray[x][y+1] == CONST_COLOR_BLACK:
            return True

        if imageArray[x][y-1] == CONST_COLOR_BLACK and imageArray[x][y+1] == CONST_COLOR_WHITE:
            return True

        if imageArray[x-1][y] == CONST_COLOR_WHITE and imageArray[x+1][y] == CONST_COLOR_BLACK:
            return True

        if imageArray[x-1][y] == CONST_COLOR_BLACK and imageArray[x+1][y] == CONST_COLOR_WHITE:
            return True



        return False

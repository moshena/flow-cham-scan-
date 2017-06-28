import objects
from datetime import datetime
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import tensorflow as tf, sys
import os


img = cv2.imread("ss.jpeg", 1)
bw = None

def main():  # here we will get image and split here to shapes +open object to save location and more

    CONST_COLOR_WHITE = 255
    CONST_COLOR_BLACK = 0
    CONST_COLOR_VOID = 2
    CONST_COLOR_RECO = 200
    CONST_COLOR_UNKOWN = 3
    CONST_COLOR_SEARCH = 14
    CONST_COLOR_LIMIT1 = 20
    CONST_COLOR_LIMIT2 = 21
    firstTime=True
    charList = []
    col = Image.fromarray(img)
    gray = col.convert('L')

    bw = np.asarray(gray).copy()
    a = np.zeros_like(bw)
    im_without_void = np.zeros_like(bw)
    im_without_void[im_without_void == 0] = 255
    # here we will try to recognize shapes

    bw[bw > 150] = 255
    bw[bw < 150] = 0
    Sentence = ""

    new_im = bw.copy()
    xsize , ysize= new_im.shape

    for x in range(0, xsize - 1):
        for y in range(0, ysize - 1):


            if (new_im[x][y] == CONST_COLOR_BLACK):

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

                    if new_im[x1, y1] == CONST_COLOR_BLACK:

                        if (x1 > maxX):
                            maxX = x1

                        if (x1 < minX):
                            minX = x1

                        if (y1 > maxY):
                            maxY = y1

                        if (y1 < minY):
                            minY = y1

                        new_im[x1, y1] = CONST_COLOR_SEARCH
                        a[x1, y1] = CONST_COLOR_WHITE

                        if x1 > 0:
                            stack.add((x1 - 1, y1))
                        if x1 < (xsize - 2):
                            stack.add((x1 + 1, y1))
                        if y1 > 0:
                            stack.add((x1, y1 - 1))
                        if y1 < (ysize - 2):
                            stack.add((x1, y1 + 1))

                imfile = Image.fromarray(new_im)

                imfile2 = Image.fromarray(a)

                if (maxX - minX < 1 or maxY - minY < 1):
                    pass
                elif (maxX < xsize and maxY < ysize):
                    if (minX - 10 > 0):
                        minX = minX-10

                    if (minY - 10 > 0):
                        minY = minY-10

                    if (maxX + 10 < xsize):
                        maxX = maxX+10

                    if (maxY + 10 < ysize):
                        maxY = maxY+10
                        now = datetime.now()

                    if(sum>250):

                        crop_img = new_im[minX:maxX, minY: maxY]
                        cv2.imwrite("object.jpeg", crop_img)
                        strResult = Recognizer(crop_img, (int)((minY + maxY) / 2), (int)((minX + maxX) / 2))
                        now = datetime.now()
                        string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]
                        cv2.imwrite(string_i_want + "a.jpeg", crop_img)
                        newchar=None

                        if(firstTime):# frame should skip
                            pass
                        else:
                            newchar = charObj(maxX,maxY,minX,minY,strResult , strResult);


                        if firstTime == False:
                            charList.append(newchar);
                        else:
                            firstTime=False
                        prevY = maxY
                        prevMaxX = maxX
                        lastmaxY = maxY - minY


    cv2.imwrite("object2.jpeg", bw)




    charlistlen = len(charList)

    for i in range (0,charlistlen):
        minObj = charList[i]
        k = i
        for t in range(i ,charlistlen):
            #print("BEFORE  miny " + str(minObj._minY) + "  tmaxy " + str(minObj._maxY) + "     tminx " + str(
            #   minObj._minX) + " tmaxx " + str(minObj._maxX));
            if ifBigThan(minObj,charList[t]):
                k = t
                minObj = charList[t]
                #print("AFTER   miny " + str(minObj._minY) + "  tmaxy " + str(minObj._maxY) + "     tminx " + str(
                 #   minObj._minX) + " tmaxx " + str(minObj._maxX));


        tempObj =  charList[k]
        charList[k] = charList[i]
        charList[i] = tempObj


    charlistlen = len(charList)
    if(charlistlen>0):
        Sentence = Sentence + " " + str(charList[0]._charName);
        spacecharsize = charList[0]._maxY-charList[0]._minY;
        prevsizey = 0;
        prevsizex = charList[0]._maxX;
    for i in range(1, charlistlen):
        prevsizespace = charList[i]._minY-charList[i-1]._maxY;
        if(charList[i]._minX>prevsizex ): #drop line
            Sentence = Sentence + " ";
        elif(prevsizespace >=spacecharsize ): #space
            Sentence = Sentence + " ";
            #print(Sentence);

        Sentence = Sentence + " " +str(charList[i]._charName);
        print(Sentence);
        prevsizex = charList[i]._maxX;
        return Sentence


    #for obj in charList:
        #print(obj._type)
        #print("miny "+str(obj._minY) + "  tmaxy "+str(obj._maxY) +"     tminx "+str(obj._minX) + " tmaxx "+str(obj._maxX));


def ifBigThan(obj1,obj2):
    # return true if obj1 apear after obj2
    if (obj1._minX > obj2._maxX):
        return True
    elif(obj2._minX > obj1._maxX):
        return False

    elif (obj1._maxY > obj2._maxY):
        return True


    return False




class charObj:#struct
    _maxX = None
    _maxY = None
    _type = None
    _charName = None
    def __init__ (self, maxx , maxy ,minx,miny, type,charName):
        self._maxX = maxx
        self._minX = minx
        self._minY = miny
        self._maxY = maxy
        self._type = type
        self._charName = charName


def Recognizer(image , xWrite , yWrite):#process engine
    # init data
    # 1. image 2.labels 3.graph
    firstCall = True
    string  = ""
    image_path = "object.jpeg"

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    if(firstCall):
        firstCall = False
        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line
                        in tf.gfile.GFile("ALPHA-BATEnglisLabels.txt")]

        # Unpersists graph from file
        with tf.gfile.FastGFile('ALPHA-BATEnglisGraph.pb', 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')


    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                        {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        flagFirst =  True
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
             #print('%s (score = %.5f)' % (human_string, score))
            if(flagFirst):
                string = human_string
                flagFirst = False

    print (string)
    return string





if __name__ == "__main__":
    main()
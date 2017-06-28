import HEADER
from PIL import Image
import numpy as np
import cv2
from datetime import datetime
import objects
from scipy import ndimage
import tensorflow as tf

DEBUGMODE = True

CONST_COLOR_WHITE = 255
CONST_COLOR_BLACK = 0
CONST_COLOR_VOID = 4
CONST_COLOR_RECO = 200
CONST_COLOR_UNKOWN = 3
CONST_COLOR_SEARCH = 244
CONST_COLOR_LIMIT1 = 20
CONST_COLOR_LIMIT2 = 21

CONST_YLINE = 1
CONST_XLINE = 2
CONST_BOTH_XYLINES = 3


CONST_SIZE_LINE = 30

ZERO_LIMIT_Y = 0
ZERO_LIMIT_X = 0
GraphFolderPath = "../data/Graphes/"


class classifier:

#images data
    imagelists = None
    image = None
    imageFilter = None
    image_data = None
#flags
    firstCall = True
    firstTimeWordRec = True
    firstCallWordRecognizer = True
    firstCallConcRecognizer = True

    STATIC_ID = 0#uniqe id per shape

    def __init__(self):
        self.image = None
        self.data = None

        self.allObjectList = []
        self.connectorList =  objects.ConnectorsList()
        self.objectList = objects.ObjectsList()

    def startProcess(self,data):# this funcation will manage the others one and return status to the caller
        self.image = data.image
        self.imageFilter = data.filteredImg
        self.data = data

        self.ObjectSpliter()

        return HEADER.unimplement

    def ObjectSpliter(self):#here we will get image and split here to shapes +open object to save location and more
        now1 = datetime.now()
        col = Image.fromarray(self.imageFilter)# convert the image to black and white
        gray = col.convert('L')

        bw = np.asarray(gray).copy()# copy the image for BACKUP
        pilot = np.zeros_like(bw)#BLACK image with the same size of the real image
        im_without_void = np.zeros_like(bw)
        im_without_void[im_without_void==0] = 255
        # here we will try to recognize shapes

        # set the array to be binary
        bw[bw> 150] = 255
        bw [bw< 150] = 0

        new_im = bw.copy()

        ZERO_LIMIT_Y = 0
        ZERO_LIMIT_X = 0
        xsize, ysize = new_im.shape
        self.data.Hboard = xsize
        self.data.Wboard = ysize

        shapeLimitsList = []

        #Clear voids
        #           run on the array end fill closed shapes after finish(each shape) send to recognize.
        #                 if the result from the recognizer is void we clear it from the picture
        #            after this loop we expect to get picture array without voids
        firstTime = True

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
                            pilot[x1,y1] = CONST_COLOR_WHITE

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
                        crop_img = pilot[minX:maxX, minY: maxY]
                        crop_img2 = new_im[minX:maxX, minY: maxY]
                        if DEBUGMODE:
                        #crop_img[crop_img2 == CONST_COLOR_WHITE] = CONST_COLOR_WHITE
                            cv2.imwrite("inves/" + string_i_want + "crop.jpeg", crop_img)
                            cv2.imwrite("inves/" + string_i_want + "crop2.jpeg",crop_img2)

                        if(sum >1000):
                            if(firstTime):
                                firstTime = False
                            else:
                                crop_img = self.fillImage(crop_img)

                            cv2.imwrite("object.jpeg", crop_img)
                            strResult =self.Recognizer(crop_img, (int)((minY + maxY) / 2), (int)((minX + maxX) / 2))
                            if DEBUGMODE:
                                cv2.imwrite("voids/" +strResult+ string_i_want + "object.jpeg", crop_img)
                            if(strResult=="void" and sum >200
                               or strResult=="voids2" and sum >200 ):
                                im_without_void=im_without_void-pilot
                                if DEBUGMODE:
                                    cv2.imwrite("trash/clear_linesChanges.png", im_without_void)
                            pilot = np.zeros_like(bw)

                            color_to_draw = 140
                            if(strResult == "void"):
                                new_im[new_im == CONST_COLOR_SEARCH] = color_to_draw
                            else:
                                new_im[new_im == CONST_COLOR_SEARCH] = CONST_COLOR_WHITE

        if DEBUGMODE:
            cv2.imwrite("trash/object.jpeg", new_im)
            cv2.imwrite("trash/image.jpeg",self.data.bwImage)
            cv2.imwrite("trash/clear_lines.png", im_without_void)
            cv2.imwrite("trash/BW.png", self.data.bwImage)

        bw = im_without_void

        im_med = ndimage.median_filter(bw, 49)

        kernel = np.ones((20, 20), np.float32) /20*20
        dst = cv2.filter2D(im_med, -1, kernel)

        dst[dst < 240] = 0
        dst[dst >= 240] = 255

        dst = dst & bw
        shapes = dst

        dst[dst < 150] = 0
        dst[dst >= 150] = 255


        dst = bw-dst

        #split and recognized shapes shapes
        #
        #      find White area send to recognize
        #      create the correct shape according to result from the recognizer
        if DEBUGMODE:
            cv2.imwrite("trash/shapesBeforeloop2.jpeg", shapes)

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
                        crop_img_wordRec = self.data.bwImage[minX:maxX, minY: maxY]

                        if (sum > 3000):
                            cv2.imwrite("object.jpeg", crop_img)
                            strResult = self.Recognizer(crop_img, (int)((minY + maxY) / 2), (int)((minX + maxX) / 2))

                            if strResult  =="square" or strResult == "rec":
                                if maxX-minX <= maxY - minY:
                                    strResult = "square"
                                else:
                                    strResult = "rec"

                            now = datetime.now()

                            string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]

                            # cv2.imwrite(string_i_want + strResult+"object.jpeg", crop_img)

                            obj = None
                            objLimits = None

                            color_to_draw = -1
                            if (strResult == "gar"):
                                color_to_draw = CONST_COLOR_UNKOWN
                            elif (strResult == "void" or strResult =="voids2"):
                                color_to_draw = CONST_COLOR_VOID
                            elif (strResult == "rec"):
                                color_to_draw = CONST_COLOR_RECO
                                recObj = objects.Rectangle(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY)
                                obj = recObj
                                self.objectList.rectangle.append(obj)
                                self.allObjectList.append(recObj)
                                objLimits = objects.objectLimits(maxX,minX,maxY,minY,self.STATIC_ID)
                            elif (strResult == "rho"):
                                color_to_draw = CONST_COLOR_RECO
                                rhoObj = objects.Rhombus(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY)
                                obj = rhoObj
                                self.objectList.rhombus.append(obj)
                                self.allObjectList.append(rhoObj)
                                objLimits = objects.objectLimits(maxX, minX, maxY, minY, self.STATIC_ID)
                            elif (strResult == "square"):
                                color_to_draw = CONST_COLOR_RECO
                                squareObj = objects.Square(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY)
                                obj = squareObj
                                self.objectList.square.append(obj)
                                self.allObjectList.append(squareObj)
                                objLimits = objects.objectLimits(maxX, minX, maxY, minY, self.STATIC_ID)
                            elif (strResult == "circle"):
                                color_to_draw = CONST_COLOR_RECO
                                circleObj = objects.Circle(self.STATIC_ID, maxY - minY, maxX - minX, minX, minY)
                                obj = circleObj
                                self.objectList.circle.append(obj)
                                self.allObjectList.append(circleObj)
                                objLimits = objects.objectLimits(maxX, minX, maxY, minY, self.STATIC_ID)

                            if (color_to_draw != CONST_COLOR_VOID and color_to_draw != CONST_COLOR_UNKOWN):
                                textInShape = self.wordrec(crop_img_wordRec)
                                obj.setText(textInShape)
                                shapes[shapes == CONST_COLOR_SEARCH] = self.STATIC_ID  + 100
                                shapeLimitsList.append(objLimits)

                                self.STATIC_ID = self.STATIC_ID + 1

                            elif(color_to_draw == CONST_COLOR_UNKOWN or color_to_draw == CONST_COLOR_VOID):
                                shapes[shapes == CONST_COLOR_SEARCH] = 0
                                color_to_draw = CONST_COLOR_RECO

                        else:
                            shapes[shapes == CONST_COLOR_SEARCH] = 0

        if DEBUGMODE:
            cv2.imwrite("trash/shapesFirstloop.jpeg", shapes)

        copmpleteImg = bw.copy()
        copmpleteImg[shapes>100] = 0
        fullImage = copmpleteImg + shapes

        if DEBUGMODE:
            cv2.imwrite("trash/fullimage.jpeg", fullImage)
        #fullImage[fullImage>200] = 255#clean changes
        fullImage[fullImage < 100] = 0

        if DEBUGMODE:
            cv2.imwrite("trash/fullimage2.jpeg", fullImage)

        # in this loop we trying to arrive from White area to area that in range 100,200
        # WHITE area - Vectors+ gar
        # range 100,200 known shapes with ID in (ID = value -100)

        stackLimitPoint = None# this stack collect the all limit area that connect between the connector and the shape- to get the id : value - 200
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
                    stackLimitPoint = set(((0, 0),))
                    adjList = []
                    sidesList = []
                    endIDsList = []
                    endSidesList = []
                    allIdList = []
                    pilot = np.zeros_like(shapes)

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

                            stackLimitPoint.add((x1,y1))# save this point for more checks
                            id = shapes[x1][y1]-100
                            pilot[x1][y1] = shapes[x1][y1]

                            FLAGExist = False
                            for adj in allIdList:
                                if adj == int(id):
                                    FLAGExist = True
                            if(FLAGExist == False):
                                TminX = None
                                TmaxX = None
                                TminY = None
                                TmaxY = None

                                offset = 40

                                if x1 -offset < 0:
                                    TminX = 0
                                else:
                                    TminX = x1 -offset

                                if y1 -offset< 0:
                                    TminY = 0
                                else :
                                    TminY = y1 -offset

                                if x1 +offset >= xsize:
                                    TmaxX = xsize -1
                                else :
                                    TmaxX = x1 +offset

                                if y1 +offset >= ysize:
                                    TmaxY = ysize -1
                                else :
                                    TmaxY = y1 +offset

                                crop_img = self.imageFilter[TminX:TmaxX, TminY: TmaxY]
                                StartArrow = False
                                allIdList.append(int(id))
                                if self.conecctorRec(crop_img) == False:
                                    adjList.append(int(id))
                                else:
                                    StartArrow = True
                                    endIDsList.append(int(id))
                                shape = None
                                for obj in self.objectList.circle:
                                    if obj._id == id:
                                        shape = obj
                                        break
                                for obj in self.objectList.rectangle:
                                    if obj._id == id:
                                        shape = obj
                                        break
                                for obj in self.objectList.square:
                                    if obj._id == id:
                                        shape = obj
                                        break
                                for obj in self.objectList.rhombus:
                                    if obj._id == id:
                                        shape = obj
                                        break

                                side = None

                                for limit in shapeLimitsList:
                                    if limit.id == id:
                                        side = self.getSide(shape, limit.maxX, limit.minX,limit.maxY, limit.minY, x1, y1)
                                        if(StartArrow and len(endSidesList) <len(endIDsList)):
                                            endSidesList.append(side)
                                            pass
                                        elif len(sidesList) <len (adjList):
                                            sidesList.append(side)
                                        break




                    tempVectorList = []
                    while (stackLimitPoint):#check if there a self connector
                        x1, y1 = stackLimitPoint.pop()
                        if pilot[x1][y1] in range(100, 200):
                            id = pilot[x1][y1] - 100
                            tempVectorList.append(id)

                            stack = set(((x1, y1),))

                            while stack:
                                tempx1, tempy1 = stack.pop()
                                if (pilot[tempx1][tempy1] in range(100, 200)):
                                    pilot[tempx1][tempy1] = pilot[tempx1][tempy1] - 100

                                    if x1 > ZERO_LIMIT_X:
                                        stack.add((tempx1 - 1, tempy1))
                                    if x1 > ZERO_LIMIT_X and y1 > ZERO_LIMIT_Y:
                                        stack.add((tempx1 - 1, tempy1-1))
                                    if x1 > ZERO_LIMIT_X and y1 < ysize-2:
                                        stack.add((tempx1 - 1, tempy1+1))
                                    if x1 < (xsize - 2):
                                        stack.add((tempx1 + 1, tempy1))
                                    if x1 < (xsize - 2) and y1< ysize-2:
                                        stack.add((tempx1 + 1, tempy1+1))
                                    if x1 < (xsize - 2) and y > 0:
                                        stack.add((tempx1 + 1, tempy1-1))
                                    if y1 > ZERO_LIMIT_Y:
                                        stack.add((tempx1, tempy1 - 1))
                                    if y1 < (ysize - 2):
                                        stack.add((tempx1, tempy1 + 1))
                    print ("[log] tempVectorList "+str(tempVectorList))
                    print ("[log] allIdList"+str(allIdList))
                    if(len(allIdList) < len(tempVectorList)):

                        for i in range (0,len(tempVectorList)):#cast to int
                            tempVectorList[i] = int(tempVectorList[i])# here need to handle the part of the self ID

                        allIdList = tempVectorList

                    if(sum > 30 and len(allIdList) > 1):
                        #need to get the entry sides
                        conc = objects.Connector(endIDsList,endSidesList,adjList,sidesList)
                        self.connectorList.connector.append(conc)
                        crop_img = bw[minX:maxX, minY: maxY]
                        if DEBUGMODE:
                            cv2.imwrite("Vectors/"+str(allIdList) + "vector"+str(self.STATIC_ID)+".jpeg", crop_img)
                        self.STATIC_ID = self.STATIC_ID+1


        self.data.objList = self.objectList
        self.data.concList = self.connectorList
        now2 = datetime.now()
        print("[log][Time] "+str(now2-now1))

    def wordrec(self,cropImage):
        if DEBUGMODE:
            cv2.imwrite("check/ basic.jpeg", cropImage)

        print("[log][classifier][wordrec]")
        self.firstTimeWordRec = True
        a = np.zeros_like(cropImage)
        charList = []
        Sentence = ""

        new_im = cropImage
        xsize, ysize = new_im.shape

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

                    if (maxX - minX < 1 or maxY - minY < 1):
                        pass
                    elif (maxX < xsize and maxY < ysize):
                        if (minX - 10 > 0):
                            minX = minX - 10

                        if (minY - 10 > 0):
                            minY = minY - 10

                        if (maxX + 10 < xsize):
                            maxX = maxX + 10

                        if (maxY + 10 < ysize):
                            maxY = maxY + 10
                            now = datetime.now()

                        if (sum > 250):
                            crop_img = a[minX:maxX, minY: maxY]
                            crop_img[crop_img == 255] = 1  # convert the colors black<->white
                            crop_img[crop_img == 0] = 255
                            crop_img[crop_img == 1] = 0
                            cv2.imwrite("object.jpeg", crop_img)
                            strResult = ""
                            now = datetime.now()
                            string_i_want = ('%02d%02d%d' % (now.minute, now.second, now.microsecond))[:-4]
                            if (self.firstTimeWordRec == False):
                                strResult = self.WordRecognizer(crop_img)
                                if DEBUGMODE:
                                     cv2.imwrite("check/ "+strResult+"  "+string_i_want + ".jpeg", crop_img)
                            elif DEBUGMODE:
                                cv2.imwrite("check/ " + string_i_want + ".jpeg", crop_img)

                            newchar = None

                            a = np.zeros_like(a)#clear the pilot

                            if (self.firstTimeWordRec):  # frame should skip
                                self.firstTimeWordRec = False
                            else:
                                newchar = objects.charObj(maxX, maxY, minX, minY, strResult, strResult);
                                charList.append(newchar);



        charlistlen = len(charList)

        for i in range(0, charlistlen):
            minObj = charList[i]
            k = i
            for t in range(i, charlistlen):
                if self.ifBigThan(minObj, charList[t]):
                    k = t
                    minObj = charList[t]


            tempObj = charList[k]
            charList[k] = charList[i]
            charList[i] = tempObj

        charlistlen = len(charList)
        if (charlistlen > 0):
            Sentence = Sentence + "" + str(charList[0]._charName);
            spacecharsize = charList[0]._maxY - charList[0]._minY;
            prevsizey = 0;
            prevsizex = charList[0]._maxX;
        for i in range(1, charlistlen):
            prevsizespace = charList[i]._minY - charList[i - 1]._maxY;
            if (charList[i]._minX > prevsizex):  # drop line
                Sentence = Sentence + " ";
            elif (prevsizespace >= spacecharsize):  # space
                Sentence = Sentence + " ";

            Sentence = Sentence + " " + str(charList[i]._charName);
            prevsizex = charList[i]._maxX;

        return Sentence

    def getSide(self,shape,maxX,maxY,minX,minY,y,x):
     #  #######################################
     # Sides return
     # for rho:
     #        /\
     #   3  /   \ 0
     #     /     \
     #     \     /
     #   2  \   / 1
     #       \/
     #
     # for circle rec and square
     #
     #        __________0____________
     #       |                      |
     #       |                      |
     #     2 |                      | 1
     #       |                      |
     #       |______________________|
     #                 3
     #
     #

        print("[log]")
        print("[log] x - " + str(x) + " y - " + str(y))
        print("[log] maxX - " + str(maxX) + " minX - " + str(minX))
        print("[log] maxY - " + str(maxY) + " minY - " + str(minY))

        if  isinstance(shape , objects.Rhombus):
            Mx = (maxX + minY)/2#middle point of rho
            My = (maxY+minY)/2

            if x> Mx:
                if y > My:
                    return 1
                else:
                    return 2
            else:
                if y > My:
                    return 0
                else:
                    return 3
        else:
            if x > minX and x < maxX:
                if y < minY:
                    return 3
                else:
                    return 1
            elif x < minX:
                return 0
            else:
                return 2

    def fillImage(self,img):

        firstcall = True

        xsize, ysize = img.shape
        fillColor = CONST_COLOR_WHITE -1
        for y in range(ZERO_LIMIT_Y, ysize - 1):
            for x in range(ZERO_LIMIT_X, xsize - 1):
                if firstcall:
                    firstcall = False
                else:
                    fillColor = CONST_COLOR_WHITE

                if (img[x][y] == CONST_COLOR_BLACK):

                    maxX = x
                    minX = x
                    maxY = y
                    minY = y
                    tempx = x
                    tempy = y
                    stack = set(((tempx, tempy),))

                    while stack:
                        x1, y1 = stack.pop()

                        if img[x1, y1] == CONST_COLOR_BLACK:

                            if (x1 > maxX):
                                maxX = x1

                            if (x1 < minX):
                                minX = x1

                            if (y1 > maxY):
                                maxY = y1

                            if (y1 < minY):
                                minY = y1

                            img[x1, y1] = fillColor

                            if x1 > ZERO_LIMIT_X:
                                stack.add((x1 - 1, y1))
                            if x1 < (xsize - 2):
                                stack.add((x1 + 1, y1))
                            if y1 > ZERO_LIMIT_Y:
                                stack.add((x1, y1 - 1))
                            if y1 < (ysize - 2):
                                stack.add((x1, y1 + 1))
        img[img == CONST_COLOR_WHITE-1] = CONST_COLOR_BLACK
        return img

    def ifBigThan(self, obj1, obj2):
        # return true if obj1 apear after obj2
        if (obj1._minX > obj2._maxX):
            return True
        elif (obj2._minX > obj1._maxX):
            return False

        elif (obj1._maxY > obj2._maxY):
            return True

        return False

    def WordRecognizer(self,crop_img):
        if DEBUGMODE:
            cv2.imwrite("inves/cropwordrec.jpeg", crop_img)

        string = ""
        image_path = "object.jpeg"

        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        if (self.firstCallWordRecognizer):
            self.firstCallWordRecognizer = False
            # Loads label file, strips off carriage return
            self.label_lines2 = [line.rstrip() for line
                           in tf.gfile.GFile(GraphFolderPath+"ALPHA-BATEnglisLabels.txt")]

            # Unpersists graph from file
            with tf.gfile.FastGFile(GraphFolderPath+'ALPHA-BATEnglisGraph.pb', 'rb') as f:
                self.graph_def2 = tf.GraphDef()
                self.graph_def2.ParseFromString(f.read())
                _ = tf.import_graph_def(self.graph_def2, name='')

        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            flagFirst = True
            for node_id in top_k:
                human_string = self.label_lines2[node_id]
                score = predictions[0][node_id]
                string = human_string
                if (self.firstCallWordRecognizer):
                    self.firstCallWordRecognizer = False

        print("[log][classifier][wordrec][recognizer] result " +string)
        return string

    def conecctorRec(self ,image):
        return True
        string = ""
        image_path = "object.jpeg"

        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        if (self.firstCallConcRecognizer):
            self.firstCallConcRecognizer = False
            # Loads label file, strips off carriage return
            self.label_lines3 = [line.rstrip() for line
                           in tf.gfile.GFile(GraphFolderPath+"concLabels.txt")]

            # Unpersists graph from file
            with tf.gfile.FastGFile(GraphFolderPath +'concGraph.pb', 'rb') as f:
                self.graph_def3 = tf.GraphDef()
                self.graph_def3.ParseFromString(f.read())
                _ = tf.import_graph_def(self.graph_def3, name='')

        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            self.firstCallConcRecognizer = True
            for node_id in top_k:
                human_string = self.label_lines3[node_id]
                score = predictions[0][node_id]
                string = human_string
                if (self.firstCallConcRecognizer):
                    self.firstCallConcRecognizer = False

        if string == "arrow":
            return True
            return False

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
                           in tf.gfile.GFile(GraphFolderPath+"shapes_labels.txt")]

            # Unpersists graph from file
            with tf.gfile.FastGFile(GraphFolderPath+'shapes_graph.pb', 'rb') as f:
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
                if(flagFirst):
                    string = human_string
                    flagFirst = False

        return string

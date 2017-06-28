import json
import copy
from PIL import Image

CONST_NUM_OF_SHAPE = 4 # 1. circle 2. rectangle 3. rhombus 4. square
CONST_NUM_OF_VECTORS_TYPE =3 # 1. vector type0 2. vector type 1 3. vector type 2

CONS_REC_NUM = 0
CONS_CRC_NUM = 1
CONS_RHO_NUM = 2
CONS_SQR_NUM = 3


CONS_CON_NUM = 0
CONS_CON1_NUM = 1
CONS_CON2_NUM = 2



class ObjectsList():

    rectangle = None
    circle = None
    rhombus = None
    square = None

    def __init__(self, *args):
        self.rectangle = []
        self.circle = []
        self.rhombus = []
        self.square = []

    def add_shape(self,shape , type):#the numbers
        if(type ==CONS_REC_NUM):
            self.rectangle.append(shape)
        elif(type ==CONS_CRC_NUM):
            self.circle.append(shape)
        elif(type==CONS_RHO_NUM):
            self.rhombus.append(shape)
        elif(type==CONS_SQR_NUM):
            self.square.append(shape)
        else: # throw Exaption
            pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

class ConnectorsList():

        connector = None


        def __init__(self, *args):
            self.connector = []


        def add_con(self,c , type):#c is the connector object and type related to kind of the connector
            if(type ==CONS_CON_NUM):
                self.connector.append(c)

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)

#unfinish code!
class objects:#struct list to save all flow chart objects
    # this class should fit the json representation and obviously every object that the list contain

    board = None#give windows size to the relvent application
    objectsList =None#1. circle 2. rectangle 3. rhombus 4. square
    connectorsList = None


    def __init__(self,boardH,boardW,objList,concList):
        self.board = Board(boardH,boardW)#1. vector type0 2. vector type 1 3. vector type 2
        self.objectsList = objList # 1. circle 2. rectangle 3. rhombus 4. square
        self.connectorsList = concList

    def toJSON(self):
         return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

    def add_rec(self,shape):
        self.objectsList.add_shape(shape,CONS_REC_NUM)

    def add_crc(self, shape):
        self.objectsList.add_shape(shape,CONS_CRC_NUM)

    def add_sqr(self, shape):
        self.objectsList.add_shape(shape,CONS_SQR_NUM)

    def add_rho(self, shape):
        self.objectsList.add_shape(shape,CONS_RHO_NUM)

    def add_con(self,shape):
        self.objectsList.add_con(shape,CONS_CON_NUM)

    def add_con1(self, shape):
        self.connectorsList.add_con(shape,CONS_CON1_NUM)

    def add_con2(self, shape):
        self.connectorsList.add_con(shape,CONS_CON2_NUM)

class Board:#struct
    _size =None

    def __init__(self,h,w):
        self._size = Size(h,w)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

class Size:#struct
    _height =None
    _width = None

    def __init__(self,h,w):
        self._height = h
        self._width = w

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

class Position:#struct
    _left = None
    _top = None
    def __init__(self,l,t):
        self._left = l
        self._top = t

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

class Objects:#abstract class

    def printme(self):
      print ("abstract Object")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

class Connector(Objects):
    #Connector is actually Vector
    _endIDs = None#list of objects IDs that connect to the connector with arrow
    _endSides = None #list that related to "_endIDs" list. the list contain the side per id`s(respectively)
    _startIDs = None#list of objects IDs that connect to the connector without arrow
    _startSides = None#list that related to "_startIDs" list. the list contain the side per id`s(respectively)

    def __init__(self,endIDs,endSides,startIDs,startSides):
        self._endID = endIDs
        self._endSide = endSides
        self._startID = startIDs
        self._startSide = startSides

    def printme(self):
      print ("Connector Object")

class Rectangle(Objects):
    _id = None
    _size = None
    _position = None
    _text = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def setText(self,txt):
        self._text = txt

    def printme(self):
        print( "Rectangle Object")

class Circle(Objects):
    _id = None
    _size = None
    _position = None
    _text = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def setText(self, txt):
        self._text = txt

    def printme(self):
        print( "Circle Object")

class Rhombus(Objects):
    _id = None
    _size = None
    _position = None
    _text = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def setText(self, txt):
        self._text = txt

    def printme(self):
        print ("Rhombus Object")

class Square(Objects):
    _id = None
    _size = None
    _position = None
    _text = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def setText(self, txt):
        self._text = txt

    def printme(self):
        print ("Square")

def get4PointsByObj(object):
    h = object._size._height
    w = object._size._width
    x = object._position._left
    y = object._position._top


    list = []

    list.append(Point(x,y))
    list.append(Point(x+w,y))
    list.append(Point(x+w,y+h))
    list.append(Point(x,y+h))

    return list

class mainData():
    PARAMSlength = None
    PARAMSlist = None
    HEADERreturn = None
    image = None
    filteredImg = None
    filteredImg2 = None
    bwImage = None

    objList = None
    concList = None
    Hboard = None
    WBoard = None


    def __init__(self, length, list):
        self.PARAMSlength= length
        self.PARAMSlist= list


    def setImage(self):
        self.image = Image.open(self.PARAMSlist[1])
        self.image = self.image.convert('L')

    def setHeader(self,header):
        self.image = header

class HEADER():
    status = None
    headerString = None

    def __init__(self, statuscode,headerString):
        self.status = statuscode
        self.headerString = headerString

class Point():
    x = None
    y = None

    def __init__(self,x,y):
        self.x = x
        self.y = y

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

class objectLimits():#this object shpukd contain the limits of specipic shape
    maxX = None
    minX = None
    maxY = None
    minY = None
    id = None

    def __init__(self, maxX,minX,maxY,minY,id):
        self.maxX = maxX
        self.minX = minX
        self.maxY = maxY
        self.minY = minY
        self.id = id



# expation unitests


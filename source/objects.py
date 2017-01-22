import json

CONST_NUM_OF_SHAPE = 4 # 1. circle 2. rectangle 3. rhombus 4. square
CONST_NUM_OF_VECTORS_TYPE =3 # 1. vector type0 2. vector type 1 3. vector type 2

#unfinish code!
class objectsList:#struct list to save all flow chart objects
    # this class should fit the json representation and obviously every object that the list contain

    board = None#give windows size to the relvent application
    objectsList =None#1. circle 2. rectangle 3. rhombus 4. square
    connectorsList = None

    def __init__(self):
        objectsList = [self.circle, self.rectangle, self.rhombus,self.square]
        connectorsList = [CONST_NUM_OF_VECTORS_TYPE]
        self.board = Board()#1. vector type0 2. vector type 1 3. vector type 2

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)


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
      print "abstract Object"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)


class Connector(Objects):

    _endID = None
    _endSide = None
    _startID = None
    _startSide = None

    def __init__(self,endID,endSide,startID,startSide):
        self._endID = endID
        self._endSide = endSide
        self._startID = startID
        self._startSide = startSide

    def printme(self):
      print"Connector Object"


class Connector1(Objects):

    _endID = None
    _endSide = None
    _startID = None
    _startSide = None

    def __init__(self,endID,endSide,startID,startSide):
        self._endID = endID
        self._endSide = endSide
        self._startID = startID
        self._startSide = startSide

    def printme(self):
      print"Vector Object"


class Connector2(Objects):

    _endID = None
    _endSide = None
    _startID = None
    _startSide = None

    def __init__(self,endID,endSide,startID,startSide):
        self._endID = endID
        self._endSide = endSide
        self._startID = startID
        self._startSide = startSide

    def printme(self):
      print"Vector Object"


class Rectangle(Objects):
    _id = None
    _size = None
    _position = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def printme(self):
        print "Rectangle Object"


class Circle(Objects):
    _id = None
    _size = None
    _position = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def printme(self):
        print "Circle Object"


class Rhombus(Objects):
    _id = None
    _size = None
    _position = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def printme(self):
        print "Rhombus Object"


class Square(Objects):
    _id = None
    _size = None
    _position = None

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def printme(self):
        print "Square"





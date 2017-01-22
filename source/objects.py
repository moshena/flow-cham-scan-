

class Size:
    _height = ""
    _width = ""

    def __init__(self,h,w):
        self._height = h
        self._width = w


class Position:
    _left = ""
    _top = ""
    def __init__(self,l,t):
        self._left = l
        self._top = t


class Objects:

    def printme(self):
      print"abstract Object"


class Vector(Objects):

    _endID = ""
    _endSide = ""
    _startID = ""
    _startSide = ""

    def __init__(self,endID,endSide,startID,startSide):
        self._endID = endID
        self._endSide = endSide
        self._startID = startID
        self._startSide = startSide

    def printme(self):
      print"Vector Object"


class Rectangle(Objects):
    _id = ""
    _size = ""
    _position = ""

    def __init__(self, id,sizeH,sizeW,posL,posT):
        self._id = id
        self._size = Size(sizeH,sizeW)
        self._position = Position(posL,posT)

    def printme(self):
        print "Vector Object"




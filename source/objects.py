import json

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
        connector2 = None
        connector3 = None

        def __init__(self, *args):
            self.connector = []
            self.connector2 = []
            self.connector3 = []


        def add_con(self,c , type):#c is the connector object and type related to kind of the connector
            if(type ==CONS_CON_NUM):
                self.connector.append(c)
            elif(type ==CONS_CON1_NUM):
                self.connector1.append(c)
            elif(type==CONS_CON2_NUM):
                self.connector2.append(c)
            else: # throw Exaption
                pass

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)

#unfinish code!
class objects:#struct list to save all flow chart objects
    # this class should fit the json representation and obviously every object that the list contain

    board = None#give windows size to the relvent application
    objectsList =None#1. circle 2. rectangle 3. rhombus 4. square
    connectorsList = None


    def __init__(self):
        self.board = Board(1100,1000)#1. vector type0 2. vector type 1 3. vector type 2
        self.objectsList = ObjectsList() # 1. circle 2. rectangle 3. rhombus 4. square
        self.connectorsList = ConnectorsList()


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



# expation unitests


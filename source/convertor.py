import objects as obj
import json as json
import os
import HEADER


from pprint import pprint


CONST_BOARD_HEIGHT_SIZE = 1100
CONST_BOARD_WIDTH_SIZE = 1000

CONS_START_STRING = """{
  "board": {
    "size": {
      "height": %s,
      "width": %s
    },
    "objectList": {"""%(CONST_BOARD_HEIGHT_SIZE,CONST_BOARD_WIDTH_SIZE)
CONST_END_STRING = """    }
  }
}

"""

CONST_RECTANGLE_STRING = """ "rectangle": ["""
CONST_RHOMBUS_STRING = """ "rhombus": ["""
CONST_CIRCLE_STRING = """ "circle": ["""
CONST_SQUARE_STRING = """ "square": ["""

CONST_START_CONNECTOR_LIST_STRING = """ "connectorsList": { """
CONST_END_CONNECTOR_LIST_STRING = """ } """

CONST_CONNECTOR_0_STRING = """ "connector": [ """
CONST_CONNECTOR_1_STRING = """ "connector1": [ """
CONST_CONNECTOR_2_STRING = """ "connector2": [ """


CONST_END_BRACKETS_STRING = """ ]"""



#unfinish code!
class convertor:

    _objList = None
    _file = None

    def __init__(self,objList):
        pass
        #self_objList = None
        #self.create_json_file()
        #self.print_to_file()

    def startProcess(self):# this funcation will manage the others one and return status to the caller
        return HEADER.unimplement

    def create_json_file(self):
        self._file = open("../tests_files/output_Json_Tests/tal.json", "wb")

    def print_to_file(self):
        file.write(self._file,CONS_START_STRING )
        file.write(self._file,CONST_END_STRING)


        count = 0
        for list in self._objList: #if we will not seccess to represent list like json we will implement this unfinish function
            if count == 0:
                file.write(self._file, CONST_RECTANGLE_STRING )
            elif count == 1:
                file.write(self._file, CONST_CIRCLE_STRING)
            elif count == 2:
                file.write(self._file, CONST_RHOMBUS_STRING )
            elif count == 3:
                file.write(self._file, CONST_SQUARE_STRING)
            elif count == 4:
                file.write(self._file, CONST_START_CONNECTOR_LIST_STRING)
                file.write(self._file, CONST_CONNECTOR_0_STRING)
            elif count == 5:
                file.write(self._file, CONST_CONNECTOR_1_STRING)
            else:
                file.write(self._file, CONST_CONNECTOR_2_STRING)


            for object in list:
                file.write(self._file, object)

            file.write(self._file, CONST_END_CONNECTOR_LIST_STRING)
            count+=1

            if count == 6:
                file.write(self._file, CONST_END_STRING)










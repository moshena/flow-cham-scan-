import objects as obj
import convertor as conv
from json import JSONEncoder

#unsinish code!

rec =obj.Rectangle(0,1,2,1,1)
list = obj.objectsList()
list.add_Rec(rec)
str1 = list.toJSON()

print(str1)
#This script create 100 images(in the path tthat the script is it) and open them with paint
#for fst run use RUNME.bat file
#after runing the script all that you need to do is to draw your shape and save them
from PIL import Image
import os

i=0
width = 400
height = 400
basicname = 'test_out'
file = open('RunPaint.bat', 'w')

for x in range(100):
    i=i+1
    img = Image.new('RGB', (width, height),'white')
    img.save(basicname +str(i)+'.png')
    file.write('mspaint '+ basicname +str(i)+'.png\n')

file.close()
os.startfile('RunPaint.bat')

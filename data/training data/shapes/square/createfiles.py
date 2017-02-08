from PIL import Image



t =1
for i in range(0,500):
    st = str(t)
    png = st+'.png'
    jp = st+'.jpg'
    im = Image.open(png)
    im.save(jp, "JPEG")
    t+=1
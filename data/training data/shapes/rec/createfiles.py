from PIL import Image



t =155
for i in range(154,500):
    st = str(t)
    png = st+'.png'
    jp = st+'.jpg'
    im = Image.open(png)
    im.save(jp, "JPEG")
    t+=1
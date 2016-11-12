from PIL import Image
img = Image.open('Media\\board3.png')
tuples = []
##for x in range(img.size[0]):
##    isfree = True
##    for y in range(img.size[1]):
##        if not (abs(img.getpixel((x,y))[0]-238)<10 and
##            abs(img.getpixel((x,y))[1]-238)<10 and
##            abs(img.getpixel((x,y))[2]-238)<10):
##            isfree = False
##    if isfree:
##        tuples.append(x)
##print tuples
    
    
img2 = img.crop((7,6,647,646))
img2.save('board1.png')

from PIL import Image, ImageDraw, ImageFont
import time
from numpy import array
import json

font_path = 'OpenSans-Regular.ttf'
font = ImageFont.truetype(font_path, 20)

def hex2rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def drawCircle(draw, mid_x, mid_y, radius, fill, label1='', label2=''):
    draw.ellipse([mid_x-radius, mid_y-radius, mid_x+radius, mid_y+radius], fill=fill)
    draw.text([mid_x, mid_y-10], label1, font=font, fill=(75,0,130), stroke_width=2, stroke_fill=(255, 255, 255))
    draw.text([mid_x, mid_y+10], label2, font=font)

def colorRegion(arr, x, y, rgb):
    """works like a magic wand - this is DFS"""
    toVisit = []
    visited = []
    toVisit.append((x, y))
    while toVisit:
        x, y = toVisit.pop()
        if (x, y) in visited or y < 0 or x < 0 or y >= h or x >= w :
            continue
        elif arr[y][x][0] > 150:
            arr[y][x] = rgb
            toAdd = [(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]
            toVisit = toAdd + toVisit
        visited.append((x, y))
    return arr
    
with Image.open('map-small.png') as im: #map-small.png is like 0.25x the original image
    arr = array(im)
    w, h = im.size

    pal = ["f94144","f3722c","f8961e","f9c74f","90be6d","43aa8b","577590"]
    pal = [hex2rgb(h) for h in pal]
    
    tic = time.process_time()
    with open('coords.json') as f:
        coords = json.load(f)
        for i, (_, (x, y)) in enumerate(coords.items()):
            colorRegion(arr, x//4, y//4, pal[i%len(pal)])

    toc = time.process_time()
    print(f'this took {toc-tic}s to color' )

    res = Image.fromarray(arr).resize((w*4, h*4))
    with Image.open('outline.png') as outline:
        res.paste(outline, mask=outline.getchannel('A'))
    
    res.show()

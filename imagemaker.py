#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
import sys
import os, cv2



def processFunc(text, OUTPUT):
    monospace = ImageFont.truetype('Inconsolata-Regular.ttf', size=8)
    picture = Image.new('RGB', (1,1))
    drawing = ImageDraw.Draw(picture)
    x,y  = (drawing.multiline_textsize(text, font=monospace))
    picture = picture.resize((x,y))
    drawing = ImageDraw.Draw(picture)
    drawing.multiline_text((0,0),text, font=monospace)

    if picture.size[0] > 852 or picture.size[1] > 480:
        picture = picture.resize((852,480))


    picture.save(OUTPUT + '.jpg')

    return(OUTPUT+".jpg")




if __name__ == "__main__":
    text = sys.argv[1]
    processFunc(text)

#!/usr/bin/env python

from vidgear.gears import VideoGear
import time
import numpy as np
import moviepy.editor as mp
from pytube import YouTube
import random
import sys




def main(link, width = 44, height = 22, frameskip = 5, mapping = "L", charset = 2):
    global SYMBOLSF, SYMBOLS, RESOLUTION, FPS, A, M, L, MAPPING, VIDLINK, SYMBOLSET
    SYMBOLS = "'^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    SYMBOLSF =  " .:-=+*#%@"
    A, M, L = "average", "min_max", "luminosity"

    if charset == 1:
        SYMBOLSET = "SYMBOLS"
    elif charset == 2:
        SYMBOLSET = "SYMBOLSF"

    RESOLUTION = (width,height)
    FPS = 1
    FRAMESKIP = frameskip
    if mapping == "A":
        MAPPING = A
    elif mapping == "M":
        MAPPING = M
    elif mapping == "L":
        MAPPING = L

#   VIDLINK = str(sys.argv[1])
    VIDLINK = link
    yield "Getting video..."
    downloadVideo(VIDLINK)
    yield "Processing video..."
    resizeVideo("video.mp4")
    video = loadVideo("videoout.mp4")
    yield "Video has been processed..."
    increment = 0
    while True:
        frame = video.read()

        if frame is None:
            yield None
            break

        #FRAME SKIP
        increment = increment + 1
        if increment % FRAMESKIP == 0:
            pixels = processPixels(frame)
            output = printPixels(pixels)
            yield output
            #so a video gets loaded into heightxwidthxrgb so its like [H][W][RGB]
            time.sleep(1/FPS)
            increment = 0

    video.stop()


def downloadVideo(link):
    yt = YouTube(link)

    stream = yt.streams.filter(res="360p", file_extension="mp4", type="video")

    if len(stream) < 1:
        raise IndexError("No streams found")
    id = random.randint(0,len(stream)-1)

    stream[id].download(filename="video.mp4")

def resizeVideo(video):
    clip = mp.VideoFileClip(video)
    clip_resized = clip.resize(RESOLUTION)
    clip_resized.write_videofile("videoout.mp4")

def loadVideo(videoname):
    stream = VideoGear(source=videoname).start()
    return stream

def goThroughVideo(video):
    while True:
        frame = video.read()

        if frame is None:
            break

        pixels = processPixels(frame)
        printPixels(pixels)
        #so a video gets loaded into heightxwidthxrgb so its like [H][W][RGB]

    video.stop()

def processPixels(frame):
    storage = np.empty([frame.shape[0],frame.shape[1]], dtype=str)
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            R = frame[x][y][2]
            G = frame[x][y][1]
            B = frame[x][y][0]
            brightness = getBrightness(R, G, B)
            symbol = getSymbol(brightness)
            #print(symbol, end="")
            #print(symbol, end="")
            #print(symbol, end="")
            storage[x][y] = str(symbol)
        #print("")
    return storage

def getSymbol(brightness):
    #for real symbols its 3.9/64
    if SYMBOLSET == "SYMBOLSF":
        index = int(round(brightness / 25.5))
        if index > 9:
            index = 9
        elif index < 0:
            index = 0
        return SYMBOLSF[index]
    elif SYMBOLSET == "SYMBOLS":
        index = int(round(brightness / 3.9))
        if index > 64:
            index = 64
        elif index < 0:
            index = 0
        return SYMBOLS[index]

def getBrightness(R, G, B):
    if MAPPING == A:
        brightness = int((R+G+B)/3)
    elif MAPPING == M:
        brightness = int(max(R, G, B) + min(R, G, B) / 2)
    elif MAPPING == L:
        brightness = int((0.21*R) +(0.72*G) + (0.07*B))
    return brightness

def printPixels(storage):
    string = ""
    for x in range(storage.shape[0]):
        for y in range(storage.shape[1]):
            string = string + (storage[x][y] * 2)
        string = string + "\n"
    return string

if __name__ == "__main__":
    main()

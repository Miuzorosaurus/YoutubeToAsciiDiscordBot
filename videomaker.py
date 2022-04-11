#!/usr/bin/env python

import time
import numpy as np
from pytube import YouTube
import random
import sys
import argparse
import cv2
from imagemaker import processFunc




def main(**kwargs):
    global SYMBOLSF, SYMBOLS, RESOLUTION, FPS, A, M, L, MAPPING, VIDLINK, SYMBOLSET, DISCORD, OUTPUT, IMAGE
    SYMBOLS = "'^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    SYMBOLSF =  " .:-=+*#%@"
    A, M, L = "average", "min_max", "luminosity"

    DISCORD = kwargs.get('discord')

    if kwargs.get("image") != None:
        IMAGEMODE = kwargs.get("image")
    else:
        IMAGEMODE = 0


    if kwargs.get('symbols') == 1:
        SYMBOLSET = "SYMBOLS"
    else:
        SYMBOLSET = "SYMBOLSF"


    if kwargs.get('width') != None:
        WIDTH = kwargs.get('width')
    else:
        if IMAGEMODE != 1:
            WIDTH = 44
        else:
            WIDTH=180

    if kwargs.get('height') != None:
        HEIGHT = kwargs.get('height')
    else:
        if IMAGEMODE != 1:
            HEIGHT = 22
        else:
            HEIGHT=90

    if kwargs.get('frameskip') != None:
        FRAMESKIP = kwargs.get('frameskip')
    else:
        FRAMESKIP = 5
    if kwargs.get('fps') != None:
        FPS = kwars.get('fps')
    else:
        FPS = 8

    RESOLUTION = (WIDTH,HEIGHT)


    if kwargs.get("mapping") == 1:
        MAPPING = A
    elif kwargs.get("mapping") == 2:
        MAPPING = M
    else:
        MAPPING = L

    if kwargs.get("output") != None:
        OUTPUT = kwargs.get("output")
    else:
        OUTPUT = "video"



    VIDLINK = kwargs.get('VideoLink')


    downloadVideo(VIDLINK)


#    video = loadVideo(OUTPUT + "out.mp4")
    video = cv2.VideoCapture(str(OUTPUT + ".mp4"))
    increment = 0

    maxattempts = 99
    attempts = 0
    if (video.isOpened() == False):
        while attempts < maxattempts and video.isOpened() == False:
            print("Error occured. Retrying..")
            downloadVideo(VIDLINK)
            video = cv2.VideoCapture(str(OUTPUT + ".mp4"))
            attempts = attempts + 1
        if attempts == maxattempts:
            print("Error has occured. Failed to open video. Exiting...")
            exit()
    attempts = 0

    while video.isOpened():
        ret, frame = video.read()

        if ret == False:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT), fx = 0, fy = 0, interpolation = cv2.INTER_AREA)

        #FRAME SKIP
        increment = increment + 1
        if increment % FRAMESKIP == 0:
            pixels = processPixels(frame)
            output = printPixels(pixels)
            if IMAGEMODE == 1:
                output = processFunc(output, OUTPUT)
            elif IMAGEMODE == 0 and discordCheck() == False:
                print(output)
            if discordCheck():
                yield output
            #so a video gets loaded into heightxwidthxrgb so its like [H][W][RGB]
            if discordCheck == False:
                time.sleep(1/FPS)
            increment = 0

    video.release()
    exit()


def discordCheck():
    if DISCORD!= None:
        return True


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("VideoLink", help="Link to the video")
    parser.add_argument("--height", type=int, help="Video height. Default is 22.")
    parser.add_argument("--width", type=int, help="Video width. Default is 44.")
    parser.add_argument("--frameskip", type=int, help="How often should frames be skipped. Default is 5.")
    parser.add_argument("-f", "--fps", type=int, help="Set how many frames per second should the program produce. Default is 8.")
    parser.add_argument("-m", "--mapping", type=int, help="Which brightness mapping method should be used. Values can be 1 for average, 2 for min-max, 3 for luminosity. Default is 3.")
    parser.add_argument("-s", "--symbols", type=int, help="Which set of symbols should be used. 1 for more symbols, 2 for less symbols. Default is 2.")
    parser.add_argument("-o", "--output", help="To what file should the video be saved, that is going to be used for processing? Default is video.mp4")
    parser.add_argument("-i", "--image", type=int, help="1 to instead output to image file, 0 to disable. Default is 0.")
    args = parser.parse_args()
    return vars(args)

def downloadVideo(link):
    yt = YouTube(link)

    stream = yt.streams.filter(res="480p", file_extension="mp4", type="video")

    if len(stream) < 1:
        raise IndexError("No streams found")
    id = random.randint(0,len(stream)-1)

    attempts = 0
    maxattempts = 5
    while attempts < maxattempts:
        try:
            stream[id].download(filename=(OUTPUT + ".mp4"))
            break
        except:
            print("Error downloading. Retrying...")
            attempts = attempts + 1
    if attempts == maxattempts:
        print("Error downloading. Exiting...")
        exit()

    
def loadVideo(videoname):
    stream = cv2.VideoCapture(videoname)
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
    args = parse()
    while True:
        output = main(**args)
        for x in output:
            print(x)

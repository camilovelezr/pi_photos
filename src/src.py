import io
import math
import time
from tkinter import *
from urllib.request import urlopen

import numpy as np
import quantumrandom
import slmpy
from gphotospy import authorize
from gphotospy.album import *
from gphotospy.media import *
from PIL import Image

CLIENT_SECRET_FILE = "credentials.json"

def find_album(album_iterator):
    for n in album_iterator:
        if (n.get("title")=="La LW"):
            return n.get("id")


GG = quantumrandom.cached_generator()

def init_photos():
    global album_media_list
    # url_time = time.time()
    service = authorize.init(CLIENT_SECRET_FILE)
    album_manager = Album(service)
    album_iterator = album_manager.list()
    _id = find_album(album_iterator)
    media_manager = Media(service)
    album_media_list = list(media_manager.search_album(_id))

def getimg(): # random for now
    n = math.floor(quantumrandom.randint(0, len(album_media_list), GG))
    url = album_media_list[n].get("baseUrl")
    img_url = f"{url}=w{1440}-h{1080}"
    img_bytes = urlopen(img_url).read()
    imgnp = np.array(Image.open(io.BytesIO(img_bytes)))
    return imgnp


def center_y(img, y):
    # check if y == 1080 and fill if not
    yi = img.shape[0]
    xi = img.shape[1]
    if yi != y:
        dy = y-yi
        if dy%2==0:
            hblack = dy//2 # height of black bar
            hblack = np.zeros([hblack, xi, 3], dtype=np.uint8) # black bar
            f_img = np.append(hblack, np.append(img, hblack, axis=0), axis=0)
        else:
            hblack = dy//2 # height of black bar bottom
            hblack = np.zeros([hblack, xi, 3], dtype=np.uint8) # black bar bottom
            htblack = y-(dy+yi) # height of black bar top 
            f_img = np.append(hblack, np.append(img, htblack, axis=0), axis=0)
        return f_img
    else:
        return img


def center(img, x, y):
    img = center_y(img, y) # check if y == 1080 and fill if not
    xi = img.shape[1]
    dx = x-xi
    even = False
    if dx%2 == 0:
        even = True
    if even:
        lblack = dx//2 # length of black needed
        black = np.zeros([y, lblack, 3], dtype=np.uint8) # np array of black (zeros)
        f_img = np.append(black, np.append(img, black, axis=1), axis=1) # final image
    else:
        lblack = dx//2 # length of black for the left
        black_left = np.zeros([y, lblack, 3], dtype=np.uint8) # np array of black (zeros) LEFT
        lblack_right = (x-(xi+lblack)) # length of black in the right
        black_right = np.zeros([y, lblack_right, 3], dtype=np.uint8) # np array of black (zeros) RIGHT
        f_img = np.append(black_left, np.append(img, black_right, axis=1), axis=1) # final image
    
    return f_img


def init():
    global slm, x, y
    slm = slmpy.SLMdisplay()
    x, y = slm.getSize()

init_photos()
init()

def test():
    global stime
    stime = time.time()

test()


def show():
    while True:
        try:
            img = getimg()
        except:
            init_photos()
            img = getimg()
        slm.updateArray(center(img, x, y))
        time.sleep(15)
        # if time.time() - url_time >= (3600):  more than one hour have passed
        #     print("60 minutes have passed")
        #     init_photos()

show() #starting at 12:05

slm.close()
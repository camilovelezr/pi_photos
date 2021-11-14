import google_auth_httplib2
from gphotospy import album, authorize

import io
from tkinter import *
from urllib.request import urlopen

from gphotospy.authorize import get_credentials
from PIL import ImageTk, Image

CLIENT_SECRET_FILE = "credentials.json"

service = authorize.init(CLIENT_SECRET_FILE)

from gphotospy.album import *

album_manager = Album(service)

album_iterator = album_manager.list()

def find_album():
    for n in album_iterator:
        if (n.get("title")=="La LW"):
            return n.get("id")

_id = find_album()

from gphotospy.media import *

media_manager = Media(service)

album_media_list = list(media_manager.search_album(_id))

len(album_media_list)

url = album_media_list[10].get("baseUrl")


root = Tk()

canvas = Canvas(root, widt=800, height=600, bg='white')

canvas.pack(side='top', fill='both', expand='yes')

im_url = f"{url}=w800-h600"

img_bytes = urlopen(im_url).read()

img = Image.open(io.BytesIO(img_bytes))

photo = ImageTk.PhotoImage(img)

canvas.create_image(10, 10, image=photo, anchor='nw')

import os
import secrets
from PIL import Image
from flask import url_for
# from flask_blog import app
from flask import current_app

#save picture update
def save_picture(form_picture):
    #randomize the name of the picture to a random hex
    random_hex = secrets.token_hex(8)
    #get the file extentsion eg jpg pg
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    #saving picture to static/
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)
    
    #resizing image to 125x125px using pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
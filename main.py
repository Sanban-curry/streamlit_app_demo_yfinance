#CAUTION YOU HAVE TO ADD YOUR COMPUTER VISION KEY AND ENDPOINT IN SECRET.JSON FILETO USE THIS APP

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os
from PIL import Image
from PIL import ImageDraw
from PIL import  ImageFont
import json

with open('secret.json') as f:
    secret = json.load(f)

KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

subscription_key = KEY
endpoint = ENDPOINT
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


#anylize image
images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

def anylize_image(file_path):
    local_image = open(file_path, "rb")
    local_image_features = ["objects", "tags"]
    return computervision_client.analyze_image_in_stream(local_image, local_image_features)

def detect_objects(anylize):
    objects = anylize.objects
    return objects

#append only tag.name to class <tags_name>
def get_tags(anylize):
    tags = anylize.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

import streamlit as st

st.title('物体検出アプリ')

uploaded_file = st.file_uploader('Choose an image...', type=['jpg','png'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    anylized_results = anylize_image(img_path)
    objects = detect_objects(anylized_results)


    #描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./AmaticSC-Regular.ttf', size=50)
        text_w, text_h = draw.textsize(caption, font=font)


        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=5)
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='green', outline='green', width=5)
        draw.text((x, y), caption, fill='white', font=font)


    st.image(img)
    tags_name = get_tags((anylized_results))
    tags_name = ', '.join(tags_name)



    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'>{tags_name}')
# -*- coding: utf-8 -*-

import os
import pprint
import sys
import yaml
from clarifai.client import ClarifaiApi

clarifai_api = ClarifaiApi()
foods = yaml.load(open(os.path.join("variables", "foods.yaml")))

def textToSpeech(text):
    print text
    if sys.platform == "win32":
        python = "py -3"
    else:
        python = "python3"
    os.system("{} tts.py creds.json ".format(python) + "\"" + text + "\"" + " output.pcm")

def get_tag_images(img_path):
    result = clarifai_api.tag_urls(img_path) if img_path.startswith("http") else clarifai_api.tag_images(open(os.path.join("img", img_path), "rb"))
    return result

def get_tags(result):
    return result.get("results")[0].get("result").get("tag").get("classes")

def get_probs(result):
    return result.get("results")[0].get("result").get("tag").get("probs")

result = get_tag_images("sunflower.jpg")
tags = get_tags(result)
probs = get_probs(result)

d = dict(zip(tags, probs))
pprint.pprint(d)

# Find tag with highest percentage of probability
r1 = max(d.iterkeys(), key=(lambda k: d[k]))
r2 =""
for tag in tags:
    if tag in foods:
        r2 = tag
        textToSpeech(r2)
if r1 != r2:
    if r2 not in foods:
        textToSpeech(r1) 






    
   

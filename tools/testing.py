# -*- coding: utf-8 -*-

import os
import pprint
import sys
import yaml
from clarifai.client import ClarifaiApi

clarifai_api = ClarifaiApi()
foods = yaml.load(open(os.path.join("tools", "variables", "foods.yaml")))

def textToSpeech(text):
    print text
    if sys.platform == "win32":
        python = "py -3"
    else:
        python = "python3"
    os.system("{} tools/tts.py tools/creds.json ".format(python) + "\"" + text + "\"" + " output.pcm")

def get_tag_images(img_path):
    result = clarifai_api.tag_urls(img_path) if img_path.startswith("http") else clarifai_api.tag_images(open(os.path.join("uploads", img_path), "rb"))
    return result

def get_tags(result):
    return result.get("results")[0].get("result").get("tag").get("classes")

def get_probs(result):
    return result.get("results")[0].get("result").get("tag").get("probs")

# result = get_tag_images("http://www.characters.ca/wp-content/uploads/2015/05/steak.jpg")
# tags = get_tags(result)
# probs = get_probs(result)

# d = dict(zip(tags, probs))
# pprint.pprint(d)

# Find tag with highest percentage of probability
# r = max(d.iterkeys(), key=(lambda k: d[k]))
# textToSpeech(r)

# for tag in tags:
#     if tag in foods:
#         textToSpeech(tag)

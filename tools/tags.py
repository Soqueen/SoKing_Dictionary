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
    return text

def get_tag_images(img_path):
    result = clarifai_api.tag_urls(img_path) if img_path.startswith("http") else clarifai_api.tag_images(open(os.path.join("uploads", img_path), "rb"))
    return result

def get_tags(result):
    return result.get("results")[0].get("result").get("tag").get("classes")

def get_probs(result):
    return result.get("results")[0].get("result").get("tag").get("probs")

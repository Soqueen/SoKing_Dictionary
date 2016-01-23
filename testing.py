
import os
import pprint
from clarifai.client import ClarifaiApi

clarifai_api = ClarifaiApi()

def textToSpeech(text):
    print text
    os.system("py -3 tts.py creds.json " + "\"" + text + "\"" + " output.pcm")

def get_tag_images(img_path):
    result = clarifai_api.tag_urls(img_path) if img_path.startswith("http") else clarifai_api.tag_images(open(os.path.join("img", img_path), "rb"))
    return result

def get_tags(result):
    return result.get("results")[0].get("result").get("tag").get("classes")

def get_probs(result):
    return result.get("results")[0].get("result").get("tag").get("probs")

result = get_tag_images("cabbage.jpg")
tags = get_tags(result)
probs = get_probs(result)

d = dict(zip(tags, probs))
pprint.pprint(d)

# Find tag with highest percentage of probability
r = max(d.iterkeys(), key=(lambda k: d[k]))

textToSpeech(r)

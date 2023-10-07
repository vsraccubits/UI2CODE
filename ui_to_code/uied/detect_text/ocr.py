import json
import time
from base64 import b64encode

import requests


def Google_OCR_makeImageData(imgpath):
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                # 'type': 'TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()


def ocr_detection_google(imgpath):
    start = time.time()
    url = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = "AIzaSyC2bX-smUQuNj5IuqUT8AflIXovLjP1Cwg"          # *** Replace with your own Key ***
    imgdata = Google_OCR_makeImageData(imgpath)
    response = requests.post(url,
                             data=imgdata,
                             params={'key': api_key},
                             headers={'Content_Type': 'application/json'})
    # print('*** Text Detection Time Taken:%.3fs ***' % (time.clock() - start))
    # print("*** Please replace the Google OCR key at detect_text/ocr.py line 28 with your own (apply in https://cloud.google.com/vision) ***")
    if 'responses' not in response.json():
        raise Exception(response.json())
    if response.json()['responses'] == [{}]:
        # No Text
        return None
    else:
        return response.json()['responses'][0]['textAnnotations'][1:]

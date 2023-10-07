from os.path import join as pjoin
import cv2
import os


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))


def element_detection(input_path_img='data/input/9.png', output_root='data/output'):

    '''
        ele:min-grad: gradient threshold to produce binary map         
        ele:ffl-block: fill-flood threshold
        ele:min-ele-area: minimum area for selected elements 
        ele:merge-contained-ele: if True, merge elements contained in others
        text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
        text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

        Tips:
        1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
        2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
        3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
        4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    '''
    key_params = {'min-grad':10, 'ffl-block':5, 'min-ele-area':25, 'merge-contained-ele':True,
                  'max-word-inline-gap':4, 'max-line-gap':4}

    # set input image path

    resized_height = resize_height_by_longest_edge(input_path_img)
    resized_height = None

    is_ip = True
    is_clf = False
    is_ocr = True
    is_merge = True

    if is_ocr:
        import uied.detect_text.text_detection as text
        import json
        os.makedirs(pjoin(output_root, 'ocr'), exist_ok=True)
        text.text_detection(input_path_img, output_root, show=True, method='google')
        output_json_path = pjoin(output_root, 'ocr', os.path.basename(input_path_img)[:-4] + '.json')
        ocr_json = json.load(open(output_json_path, 'r'))
        output_json = {"compos": []}
        for text_data in ocr_json["texts"]:
            compos_data = {
                "row_max": text_data["row_max"],
                "column_min": text_data["column_min"],
                "column_max": text_data["column_max"],
                "row_min": text_data["row_min"]
            }
            output_json["compos"].append(compos_data)
        json.dump(output_json, open(output_json_path, 'w'), indent=4)

    if is_ip:
        import uied.detect_compo.ip_region_proposal as ip
        os.makedirs(pjoin(output_root, 'ip'), exist_ok=True)
        # switch of the classification func
        classifier = None
        if is_clf:
            classifier = {}
            from cnn.CNN import CNN
            # classifier['Image'] = CNN('Image')
            classifier['Elements'] = CNN('Elements')
            # classifier['Noise'] = CNN('Noise')
        ip.compo_detection(input_path_img, output_root, key_params,
                           classifier=classifier, resize_by_height=None, show=False)

    if is_merge:
        from uied import merge
        name = input_path_img.split('/')[-1][:-4]
        compo_path = pjoin(output_root, 'ip', str(name) + '.json')
        ocr_path = pjoin(output_root, 'ocr', str(name) + '.json')
        merge.incorporate(input_path_img, compo_path, ocr_path, output_root, params=key_params,
                          resize_by_height=None, show=True)
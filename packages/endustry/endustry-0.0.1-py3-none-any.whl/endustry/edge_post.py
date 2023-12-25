import requests
import cv2

from tools import im_to_base64
from atomic_capability import atomic_capabilitys_info as info


class EdgePost(object):
    def __init__(self, img, url, mode):
        self.img = im_to_base64(img)
        self.url = url
        self.headers = self.get_headers()
        self.json = self.get_body()
        self.mode = mode
        self.return_template = self.get_return_template()

    def get_headers(self):
        headers = {"Content-Type": "application/json"}

        return headers

    def get_body(self):
        body = {
            "images": self.img
        }

        return body

    def get_return_template(self):
        if self.mode == "OD":
            return_template = info["object_detection"].get("output_template")
        elif self.mode == "PE":
            return_template = info["object_detection"].get("pose estimatio")
        elif self.mode == "IC":
            return_template = info["object_detection"].get("image classification")
        elif self.mode == "AD":
            return_template = info["object_detection"].get("anomaly detection")
        elif self.mode == "OT":
            return_template = info["object_detection"].get("object tracking")
        elif self.mode == "OT":
            return_template = info["object_detection"].get("semantic segmentation")
        elif self.mode == "OT":
            return_template = info["object_detection"].get("instance segmentation")
        else:
            return None

        return return_template

    def post(self):
        response = requests.post(url=self.url, headers=self.headers, json=self.json)

        return response


if __name__ == "__main__":
    img = cv2.imread("../img/apitest.jpg")
    url = 'http://172.27.254.2:32465'
    EPOD = EdgePostOD(img, url, mode="OD")
    output = EPOD.post()

    print(output)

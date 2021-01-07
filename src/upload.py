import base64
import os

base_path = os.path.join('assets', 'image_files')
if not os.path.exists(base_path):
    os.mkdir(base_path)


def download_image_from_upload(name, data):
    image_path = os.path.join(base_path, name)
    data_encoded = data.encode("utf8").split(b";base64,")[1]

    with open(os.path.join(os.getcwd(), image_path), "wb") as fh:
        fh.write(base64.decodebytes(data_encoded))

    return image_path

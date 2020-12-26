import base64
import os

if os.path.exists('assets/image_files'):
    import shutil
    shutil.rmtree('assets/image_files')

base_path = os.path.join(os.getcwd(), 'assets/image_files')
if not os.path.exists(base_path):
    os.mkdir(base_path)


def download_image_from_upload(name, data):
    image_path = os.path.join(base_path, f"{name}.jpeg")
    data_encoded = data.encode("utf8").split(b";base64,")[1]

    with open(image_path, "wb") as fh:
        fh.write(base64.decodebytes(data_encoded))

    return image_path

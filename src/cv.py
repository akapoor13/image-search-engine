import cv2
import numpy as np
import json
import src.constants as const

detector = cv2.SIFT_create()

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(check=50)  # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)


def sift_descriptor(image, detector=detector):
    """
        return keypoint and descriptor of an image
    """
    _, des = detector.detectAndCompute(image, None)

    return des


def sift_descriptors_path(path):
    """
        sift descriptors as json structure to save in db from an image path
    """
    img = cv2.imread(path)
    des = sift_descriptor(img)
    json_des = json.dumps(des.tolist(), separators=(',', ':'), indent=0)

    return json_des


def flann_matches(des1, des2, k=2, matcher=flann):
    """
        flann matches for a target image description and a test image description
    """
    des1 = np.array(des1)
    des1 = des1.astype(np.float32)

    des2 = np.array(des2)
    des2 = des2.astype(np.float32)

    matches = matcher.knnMatch(des1, des2, k)

    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append((m, n))

    return good


def histogram(image, mask, bins=(8, 12, 3)):
    """
        build 3D color descriptor for histogram
    """
    hist = cv2.calcHist([image], [0, 1, 2], mask, bins,
                        [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    return hist


def chi2_distance(histA, histB, eps=1e-10):
    """
        compare image histograms for similarity
    """
    d = 0.5 * np.sum([((a - b)**2) / (a + b + eps)
                      for (a, b) in zip(histA, histB)])

    return d


def color_descriptor(image):
    """
        build color descriptor for an image
    """
    features = []
    h, w = image.shape[:2]
    cX, cY = int(w * 0.5), int(h * 0.5)

    segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

    axesX, axesY = int(w * 0.75) // 2, int(h * 0.75) // 2
    ellipMask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

    for startX, endX, startY, endY in segments:
        cornerMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
        cornerMask = cv2.subtract(cornerMask, ellipMask)

        hist = histogram(image, cornerMask)
        features.extend(hist)

    hist = histogram(image, ellipMask)
    features.extend(hist)

    return features


def color_descriptor_path(path):
    """
        build color descriptor json for db from image path
    """
    img = cv2.imread(path)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    features = color_descriptor(image)

    mapped_features = list(map(float, features))
    json_features = json.dumps(mapped_features,
                               separators=(',', ':'),
                               indent=0)

    return json_features


def image_matches(df, path):
    """
        build target image descriptors and compare with test images
    """

    image = cv2.imread(path)

    target_sift_desc = sift_descriptor(image)
    target_color_desc = color_descriptor(image)

    sift_descriptors_list = df[const.SIFTDESCRIPTOR_].apply(
        lambda x: json.loads(x))
    color_descriptors_list = df[const.COLORDESCRIPTOR_].apply(
        lambda x: json.loads(x))

    flann_match = [
        len(flann_matches(i, target_sift_desc)) for i in sift_descriptors_list
    ]
    color_distance = [
        round(chi2_distance(i, target_color_desc), 2)
        for i in color_descriptors_list
    ]

    df['flann_matches'] = flann_match
    df['similarity_score'] = color_distance

    df = df[df['flann_matches'] > 5]

    return df.sort_values('similarity_score')
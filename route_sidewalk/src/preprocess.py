import cv2
import numpy as np
import matplotlib.pyplot as plt


def imread(path):
    """
    Read image and transform to usable format.

    Args:
        path: path to image

    Returns:
        image (BGR) and gray
    """

    img = cv2.imread(path)
    img = img[:-50, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img, gray


def imshow(img):
    """
    Display image.

    Args:
        img: image array
    """

    plt.figure(figsize=(20, 20))
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()


def filter_color_hsv(img, lower=[0, 0, 0], upper=[255, 255, 255]):
    """
    Filter color from image with hsv color range.

    Args:
        img: image array
        lower: [h, s, v] the lower bound for filter
        upper: [h, s, v] the upper bound for filter

    Returns:
        image after filter
    """

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, np.array(lower), np.array(upper))
    res = cv2.bitwise_and(img, img, mask=mask)

    # to gray scale
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    res = (res != 0) * 255
    res = res.astype(np.uint8)

    return res


def find_contour(img, sensitive=500):
    """
    Find contour in image.

    Args:
        img: image array
        sensitive: sensitive value for filter the contour

    Returns:
        List of Coordinates for each contours
    """

    conts, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    listx = []
    listy = []

    for i in range(0, len(conts)):
        c = conts[i]
        size = cv2.contourArea(c)
        if size < sensitive:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            listx.append(cY)
            listy.append(cX)

    listxy = list(zip(listx, listy))
    return listxy


def plot_line_with_path(img, paths, d=3, return_array=False):
    """
    Plot the line from paths

    Args:
        img: the image for reference
        paths: list of path
        d: size of path
    """

    img_tmp = np.copy(img)

    for p in paths:
        for i in range(-d + 1, d, 1):
            for j in range(-d + 1, d, 1):
                if 0 <= p[0] + i < img_tmp.shape[0] and 0 <= p[1] + j < img_tmp.shape[1]:
                    if len(img_tmp.shape) == 3:
                        img_tmp[p[0] + i, p[1] + j, :] = (255, 0, 0)
                    else:
                        img_tmp[p[0] + i, p[1] + j] = 200

    imshow(img_tmp)

    if return_array:
        return img_tmp


def process_bg(path):
    """
    Get a road from image

    Args:
        path: path to image

    Returns:
        segment road
    """

    img_map, map_gray = imread(path)

    ######## ROAD COLOR ########
    # TODO: get more support colors
    # yellow
    tmp_yellow = filter_color_hsv(img_map, [80, 60, 0], [100, 255, 255])
    kernel = np.ones((10, 10), np.uint8)
    tmp_yellow = cv2.dilate(tmp_yellow, kernel, iterations=1)

    # gold
    tmp_gold = filter_color_hsv(img_map, [100, 50, 0], [150, 100, 255])
    kernel = np.ones((10, 10), np.uint8)
    tmp_gold = cv2.dilate(tmp_gold, kernel, iterations=1)

    # white
    road_thresh = filter_color_hsv(img_map, [0, 0, 0], [255, 0, 255])
    kernel = np.ones((10, 10), np.uint8)
    road_thresh = cv2.dilate(road_thresh, kernel, iterations=1)

    # merge road
    road_thresh = cv2.bitwise_or(tmp_yellow, road_thresh)
    road_thresh = cv2.bitwise_or(tmp_gold, road_thresh)

    return img_map, road_thresh


def process_target(path):
    """
    Get coordinate of target

    Args:
        path: path to image

    Returns:
        coordinates
    """

    img_target, target_gray = imread(path)

    # dilate image
    target_segment = filter_color_hsv(img_target, [0, 10, 245], [30, 255, 255])
    kernel = np.ones((10,10), np.uint8)
    target_segment_di = cv2.dilate(target_segment, kernel, iterations=1)

    contours = find_contour(target_segment_di)

    return contours

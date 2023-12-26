from urllib.request import urlopen

import cv2
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

common_color = np.array([0., 1., 228 / 255, 0.5]).reshape(1, 1, -1)

def show_mask(mask, ax):
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * common_color
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    coords = np.asarray(coords)
    labels = np.asarray(labels)

    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
               linewidth=3)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
               linewidth=3)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


def read_from_url(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, -1)


class TqdmUpTo(tqdm):
    def __init__(self, desc: str = None):
        super().__init__(unit='B', unit_divisor=1024, miniters=1, unit_scale=True, desc=desc)

    def update_to(self, byte_consumed, total_bytes):
        if total_bytes is not None:
            self.total = total_bytes
        return self.update(byte_consumed - self.n)  # also sets self.n = b * bsize

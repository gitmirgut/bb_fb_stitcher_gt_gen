import cv2
import point_picker
from fb_stitcher.rotator import Rotator
from logging import getLogger


log = getLogger(__name__)


class GroundTruthGenerator(object):
    """Class to generate Ground-Truth data for bb_fb_stitcher."""

    def __init__(self, img_l, img_r, angle_l=90, angle_r=-90):
        rt = Rotator()
        self.img_l = rt.rotate_image(img_l, angle_l)
        self.img_r = rt.rotate_image(img_r, angle_r)

    def get_point_pairs(self):
        adj = point_picker.PointPicker(self.img_l, self.img_r)
        adj.pick()


def main():
    img_l = cv2.imread("Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.jpg")
    img_r = cv2.imread("Cam_1_2016-07-19T12:41:22.685374Z--2016-07-19T12:47:02.533678Z.jpg")
    gt = GroundTruthGenerator(img_l, img_r, 90, -90)
    gt.get_point_pairs()


if __name__ == '__main__':
    main()

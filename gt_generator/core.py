import cv2
import gt_generator.point_picker as point_picker
import numpy as np
from fb_stitcher.rotator import Rotator
from logging import getLogger
import cv2
import datetime
import json
import os


log = getLogger(__name__)


class GroundTruthGenerator(object):
    """Class to generate Ground-Truth data for bb_fb_stitcher."""

    def __init__(self, left_path=None, right_path=None, left_angle=None, right_angle=None):
        self.angle_left = left_angle
        self.angle_right = right_angle
        self.left_path = left_path
        self.right_path = right_path
        self.points_left = None
        self.points_right = None

    def get_point_pairs(self):
        img_l = cv2.imread(self.left_path, -1)
        img_r = cv2.imread(self.right_path, -1)
        rt = Rotator()
        rot_img_l = rt.rotate_image(img_l, self.angle_left)
        rot_img_r = rt.rotate_image(img_r, self.angle_right)
        adj = point_picker.PointPicker(rot_img_l, rot_img_r)
        points_left, points_right = adj.pick()
        rt = Rotator()
        self.points_left = rt.rotate_points(points_left, -self.angle_left, rot_img_l.shape)
        self.points_right = rt.rotate_points(points_right, -self.angle_right, rot_img_r.shape)
        return self.points_left, self.points_right

    def save_2_json(self, path):
        date_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        dict = {
                'date_created': date_created,
                'left_image': os.path.basename(self.left_path),
                'right_image': os.path.basename(self.right_path),
                'left_angle': self.angle_left,
                'right_angle': self.angle_right,
                'points_left': self.points_left.tolist(),
                'points_right': self.points_right.tolist()
            }

        with open(path, 'w', newline='') as jsonfile:
            json.dump(dict, jsonfile, indent=2, sort_keys=False)

    def load_json(path):
        with open(path, 'r') as jsonfile:
            d = json.load(jsonfile)
        data = {
            'date_created': d['date_created'],
            'left_image': d['left_image'],
            'right_image': d['right_image'],
            'left_angle': d['left_angle'],
            'right_angle': d['right_angle'],
            'points_left': np.array(d['points_left']),
            'points_right': np.array(d['points_right'])
        }
        return data
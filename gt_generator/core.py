import cv2
import gt_generator.point_picker as point_picker
import numpy as np
from fb_stitcher.rotator import Rotator
from logging import getLogger
import csv
import datetime
import json


log = getLogger(__name__)


class GroundTruthGenerator(object):
    """Class to generate Ground-Truth data for bb_fb_stitcher."""

    def __init__(self, angle_l=90, angle_r=-90):
        self.angle_left = angle_l
        self.angle_right = angle_r


        self.points_left = None
        self.points_right = None

    def get_point_pairs(self, img_l, img_r):
        rt = Rotator()
        rot_img_l = rt.rotate_image(img_l, self.angle_left)
        rot_img_r = rt.rotate_image(img_r, self.angle_right)
        adj = point_picker.PointPicker(rot_img_l, rot_img_r)
        points_left, points_right = adj.pick()
        rt = Rotator()
        self.points_left = rt.rotate_points(points_left, -self.angle_left, rot_img_l.shape)
        self.points_right = rt.rotate_points(points_right, -self.angle_right, rot_img_r.shape)
        return self.points_left, self.points_right

    def save_data(self, path):
        np.savez(path,
                 points_left = self.points_left,
                 points_right=self.points_right,
                 angle_left= self.angle_left,
                 angle_right= self.angle_right
                 )

    def load_data(self, path):
        with np.load(path) as data:
            self.points_left = data['points_left']
            self.points_right = data['points_right']
            self.angle_left = data['angle_left']
            self.angle_right = data['angle_right']

    @DeprecationWarning
    def save_2_csv(self, path):
        date_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['date_created', 'left_image', 'right_image', 'left_angle', 'right_angle', 'points_left', 'points_right']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerow({
                'date_created': date_created,
                'left_image': '',
                'right_image': '',
                'left_angle': self.angle_left,
                'right_angle': self.angle_right,
                'points_left': self.points_left.tolist(),
                'points_right': self.points_right.tolist()
            })

    @DeprecationWarning
    def load_csv(self, path):
        with open(path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                print(row['points_left'])
                points = np.fromstring(row['points_left'])
                print(points)

    def save_2_json(self, path):
        date_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        dict = {
                'date_created': date_created,
                'left_image': '',
                'right_image': '',
                'left_angle': self.angle_left.tolist(),
                'right_angle': self.angle_right.tolist(),
                'points_left': self.points_left.tolist(),
                'points_right': self.points_right.tolist()
            }

        with open(path, 'w', newline='') as jsonfile:
            json.dump(dict, jsonfile, indent=2, sort_keys=False)

    def load_json(self, path):
        with open(path, 'r') as jsonfile:
            d = json.load(jsonfile)
            print(np.array(d['points_left']))


def draw_makers(img, pts, color=(0, 0, 255),
                marker_types=cv2.MARKER_TILTED_CROSS):
    img_m = np.copy(img)
    pts = pts[0].astype(int)
    for pt in pts:
        cv2.drawMarker(img_m, tuple(pt), color, markerType=marker_types,
                       markerSize=40, thickness=5)
    return img_m

def main():
    img_l = cv2.imread("Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.jpg")
    img_r = cv2.imread("Cam_1_2016-07-19T12:41:22.685374Z--2016-07-19T12:47:02.533678Z.jpg")
    gt = GroundTruthGenerator(img_l, img_r, 90, -90)
    points_left, points_right = gt.get_point_pairs()
    print(points_left)
    print(points_right)
    img = draw_makers(img_l, points_left)
    cv2.imwrite('test.jpg', img)
    # cv2.waitKey()


if __name__ == '__main__':
    main()

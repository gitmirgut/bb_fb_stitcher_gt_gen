import cv2
import gt_generator.point_picker as point_picker
import numpy as np
from fb_stitcher.rotator import Rotator
from logging import getLogger
import datetime
import os
import csv
import ast
import gt_generator.helpers as helpers


log = getLogger(__name__)


class GroundTruthGenerator(object):
    """Class to generate Ground-Truth data for bb_fb_stitcher."""

    def __init__(self, left_path=None, right_path=None, left_angle=None, right_angle=None, path_csv=None, draw_old_points=True):
        self.angle_left = left_angle
        self.angle_right = right_angle
        self.left_path = left_path
        self.right_path = right_path
        self.points_left = None
        self.points_right = None
        self.entries=[]
        self.left_entries_id = []
        self.right_entries_id = []
        self.path_csv = path_csv
        self.__load_csv()

        # New implementation #TODO draw_old Points setzen
        self.draw_old_points = draw_old_points
        self.entry_ids, self.csv_points_left, self.csv_points_right = GroundTruthGenerator.get_old_data(self.entries, self.left_path, self.right_path)


    def get_point_pairs(self):

        img_l = cv2.imread(self.left_path, -1)
        img_r = cv2.imread(self.right_path, -1)

        rt = Rotator()

        if self.csv_points_left is not None and self.csv_points_right is not None:
            img_l = helpers.draw_makers(img_l, self.csv_points_left)
            img_r = helpers.draw_makers(img_r, self.csv_points_right)

        rot_img_l = rt.rotate_image(img_l, self.angle_left)
        rot_img_r = rt.rotate_image(img_r, self.angle_right)

        adj = point_picker.PointPicker(rot_img_l, rot_img_r)
        points_left, points_right = adj.pick()
        rt = Rotator()
        self.points_left = rt.rotate_points(points_left, -self.angle_left, rot_img_l.shape)
        self.points_right = rt.rotate_points(points_right, -self.angle_right, rot_img_r.shape)
        return self.points_left, self.points_right

    def save_2_csv(self):
        date_created = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        file_exists = os.path.isfile(self.path_csv)
        last_id = 1

        # check if the file was already create if yes, increment id
        if file_exists:
            last_id = int(open(self.path_csv).readlines()[-1].split(';', maxsplit=1)[0])
            last_id += 1


        with open(self.path_csv, 'a+', newline='') as csvfile:
            fieldnames = ['id','date_created', 'left_image', 'right_image', 'left_angle', 'right_angle', 'points_left', 'points_right']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            # write header if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'id': str(last_id).zfill(4),
                'date_created': date_created,
                'left_image': os.path.basename(self.left_path),
                'right_image': os.path.basename(self.right_path),
                'left_angle': self.angle_left,
                'right_angle': self.angle_right,
                'points_left': self.points_left.tolist(),
                'points_right': self.points_right.tolist()
            })

    def __load_csv(self):
        """Return a list of datasets as dicts."""
        self.entries = []
        if self.path_csv is None or not os.path.isfile(self.path_csv):
            return self.entries
        with open(self.path_csv, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                data = {
                    'id': int(row['id']),
                    'date_created': row['date_created'],
                    'left_image': row['left_image'],
                    'right_image': row['right_image'],
                    'left_angle': int(row['left_angle']),
                    'right_angle': int(row['right_angle']),
                    'points_left': np.array(ast.literal_eval(row['points_left'])),
                    'points_right': np.array(ast.literal_eval(row['points_right']))
                }
                self.entries.append(data)
        return self.entries


    @staticmethod
    def get_old_data(entries, left_filename, right_filename):
        left_basename = os.path.basename(left_filename)
        right_basename = os.path.basename(right_filename)
        left_old_points = None
        right_old_points = None
        entry_ids = None
        for entry in entries:
            if left_basename == entry['left_image']:
                assert right_basename == entry['right_image']
                if entry_ids is None:
                    assert left_old_points is None and right_old_points is None and len(entry['points_left'][0]) == len(entry['points_right'][0])
                    entry_ids = [entry['id']]
                    left_old_points = entry['points_left'][0]
                    right_old_points = entry['points_right'][0]
                else:
                    assert len(entry['points_left'][0]) == len(entry['points_right'][0])
                    entry_ids.append(entry['id'])
                    left_old_points = np.vstack((left_old_points, entry['points_left'][0]))
                    right_old_points = np.vstack((right_old_points, entry['points_right'][0]))
        if left_old_points is None:
            assert right_old_points is None and entry_ids is None
            return None, None, None
        return entry_ids, np.array([left_old_points]), np.array([right_old_points])

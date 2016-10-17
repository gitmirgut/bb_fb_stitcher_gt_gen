import cv2
import gt_generator.point_picker as point_picker
import numpy as np
from fb_stitcher.rotator import Rotator
from logging import getLogger
import datetime
import json
import os
import csv
import ast


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
        self.left_entries_id, self.right_entries_id = self.__get_existing_entries()
        if len(self.left_entries_id) + len(self.right_entries_id) > 0:
            print("There exist entries based on same images lef: {} right: {}".format(self.left_entries_id, self.right_entries_id))
        self.left_old_pts = None
        self.right_old_pts = None
        self.draw_old_points = draw_old_points
        if self.draw_old_points:
            self.left_old_pts, self.right_old_pts = self.get_old_points()
        print(self.left_old_pts)

    def get_point_pairs(self):

        img_l = cv2.imread(self.left_path, -1)
        img_r = cv2.imread(self.right_path, -1)

        rt = Rotator()
        if self.draw_old_points and self.left_old_pts is not None:
            rot_left_old_pts = rt.rotate_points(self.left_old_pts, self.angle_left, img_l.shape)
            rot_right_old_pts = rt.rotate_points(self.right_old_pts, self.angle_right, img_r.shape)
        else:
            rot_left_old_pts = None
            rot_right_old_pts = None
        rot_img_l = rt.rotate_image(img_l, self.angle_left)
        rot_img_r = rt.rotate_image(img_r, self.angle_right)

        adj = point_picker.PointPicker(rot_img_l, rot_img_r, rot_left_old_pts, rot_right_old_pts)
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

    def __get_existing_entries(self):
        """Return ids of datasets  which already exist for the images."""
        left_basename = os.path.basename(self.left_path)
        right_basename = os.path.basename(self.right_path)
        self.left_entries_id = []
        self.right_entries_id = []
        for entry in self.entries:
            image_names = [entry['left_image'], entry['right_image']]
            if left_basename in image_names:
                self.left_entries_id.append(entry['id'])
            if right_basename in image_names:
                self.right_entries_id.append(entry['id'])

        return self.left_entries_id, self.right_entries_id

    def get_old_points(self):
        left_old_points = None
        right_old_points = None
        if len(self.entries) > 0 and self.left_entries_id:
            for left_entry_id in self.left_entries_id:
                for entry in self.entries:
                    if left_entry_id == entry['id']:
                        if left_old_points is None:
                            left_old_points = entry['points_left'][0]
                        else:
                            left_old_points = np.vstack((left_old_points, entry['points_left'][0]))
        if len(self.entries) > 0 and self.right_entries_id:
            for right_entry_id in self.right_entries_id:
                for entry in self.entries:
                    if right_entry_id == entry['id']:
                        if right_old_points is None:
                            right_old_points = entry['points_right'][0]
                        else:
                            right_old_points = np.vstack((right_old_points, entry['points_right'][0]))
        if left_old_points is not None:
            left_old_points = np.array([left_old_points])
        if right_old_points is not None:
            right_old_points = np.array([right_old_points])
        return left_old_points, right_old_points

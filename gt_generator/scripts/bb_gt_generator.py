import fb_stitcher.core as core
from fb_stitcher.stitcher import Transformation
import gt_generator.core as core
import gt_generator .helpers
import argparse
import fb_stitcher.helpers
import cv2
from argparse import RawTextHelpFormatter
import os

def process_images(args):
    # checks if filenames are valid
    assert fb_stitcher.helpers.check_filename(args.left) and fb_stitcher.helpers.check_filename(args.right)



    pp = core.GroundTruthGenerator(args.left, args.right, args.left_angle, args.right_angle, args.data)
    pts_left, pts_right = pp.get_point_pairs()
    pp.request_2_save()


def main():
    parser = argparse.ArgumentParser(
        prog = 'BeesBook Ground Truth Generator for Evaluation of Stitcher.',
        description = 'Mark Points as equal.',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('left', help='Path of the left image.', type=str)
    parser.add_argument('right', help='Path of the left image.', type=str)
    parser.add_argument('left_angle', help='Rotation angle of the left image', type=int)
    parser.add_argument('right_angle', help='Rotation angle of the right image', type=int)
    parser.add_argument('data', help='Output directory/path of the points data.', type=str)

    args = parser.parse_args()
    process_images(args)

if __name__ == '__main__':
    main()

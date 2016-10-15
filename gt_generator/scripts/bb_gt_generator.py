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

    if os.path.isdir(args.data):
        start_time_l = fb_stitcher.helpers.get_start_datetime(args.left)
        start_time_r = fb_stitcher.helpers.get_start_datetime(args.right)
        output_path = ''.join([start_time_l, '_GT_', start_time_r, '.json'])
        file_path = os.path.join(args.data, output_path)
    else:
        file_path = args.data

    pp = core.GroundTruthGenerator(args.left, args.right, args.left_angle, args.right_angle)
    pts_left, pts_right = pp.get_point_pairs()

    pp.save_2_json(file_path)
    print('Saved points coordinates to: {} '.format(file_path))

    if args.pano is not None:
        if os.path.isdir(args.pano[0]):
            print(args.pano)
            img_l = cv2.imread(args.left, -1)
            img_r = cv2.imread(args.right, -1)
            img_l_marked = gt_generator.helpers.draw_makers(img_l, pts_left)
            img_r_marked = gt_generator.helpers.draw_makers(img_r, pts_right)

            output_path_left = os.path.join(args.pano[0], start_time_l + '_marked.jpg')
            output_path_right = os.path.join(args.pano[0], start_time_r + '_marked.jpg')

            cv2.imwrite(output_path_left, img_l_marked)
            cv2.imwrite(output_path_right, img_r_marked)

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
    parser.add_argument('--pano', '-p', nargs=1, help='Path of the marked images.')

    args = parser.parse_args()
    process_images(args)

if __name__ == '__main__':
    main()

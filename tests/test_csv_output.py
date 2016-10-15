import gt_generator.core as core

gt = core.GroundTruthGenerator()
# gt.load_data('data/test_csv_output/Input/Cam_0_2016-07-26T13:07:48.522458Z_GT_Cam_1_2016-07-26T13:07:48.521660Z.npz')
# gt.save_2_csv('/mnt/myStorage/bb_fb_stitcher_gt_gen/tests/data/test_csv_output/Output/data.csv')
# gt.load_csv('/mnt/myStorage/bb_fb_stitcher_gt_gen/tests/data/test_csv_output/Output/data.csv')
# gt.save_2_json('/mnt/myStorage/bb_fb_stitcher_gt_gen/tests/data/test_csv_output/Output/data.json')
core.GroundTruthGenerator.load_json('/mnt/myStorage/bb_fb_stitcher_gt_gen/tests/data/test_csv_output/Output/data.json')


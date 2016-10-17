import gt_generator.core as core


img_l_path = 'data/test_core/Input/Cam_0_2016-09-01T14:20:38.410765Z--2016-09-01T14:26:18.257648Z.jpg'
img_r_path = 'data/test_core/Input/Cam_1_2016-09-01T14:16:13.311603Z--2016-09-01T14:21:53.157900Z.jpg'
pp = core.GroundTruthGenerator(img_l_path, img_r_path, 90, -90,'data/test_core/Output/out_core.csv')
pp.get_old_points
pp.get_point_pairs()
pp.save_2_csv()
# pp.__load_csv()
# print(pp.__get_existing_entries())
print(pp.get_old_points())
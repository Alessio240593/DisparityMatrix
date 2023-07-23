from lib import image_processing as imgProc, distributions as dist

MAX_QUANTITY = 10

left_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_left.mp4', max_quantity=MAX_QUANTITY)
right_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_right.mp4', max_quantity=MAX_QUANTITY)
disparities = imgProc.from_stereo_to_disparity_matrix(left_img_list, right_img_list, save=True, destination_dir="disparity")
dist.distribution_of_frame(disparities)
dist.distribution_of_differences_over_time(disparities)
dist.distribution_of_rows_differences(disparities)
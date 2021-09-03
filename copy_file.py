import os
from airway_lobe_merge import add_label
from nii_resample import resample
from nii2npz import nii2npz
from tqdm import trange


def get_listdir(path):  # 获取目录下所有gz格式文件的地址，返回地址list
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def get_list(path):
    tmp_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        tmp_list.append(file_path)
    return tmp_list


resample_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\resample'
resample_list = get_listdir(resample_path)
resample_list.sort()
save_path = r'D:\my_code\airway_segmentation\stage1'
save_list = get_list(save_path)
save_list.sort()

for i in trange(len(resample_list)):
    nii2npz(resample_list[i], save_list[i])

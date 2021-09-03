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


if __name__ == '__main__':
    airway_path = r'F:\segment_registration\Registration\original_image\airway_masks'  # 气道树mask
    airway_list = get_listdir(airway_path)
    airway_list.sort()
    lobe_path = r'F:\segment_registration\Registration\original_image\lobe_masks'  # 由nnUnet分割得出的肺叶mask
    lobe_list = get_listdir(lobe_path)
    lobe_list.sort()
    lobe_airway_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\lobe_airway_masks'  # 气道树和肺叶融合后mask路径
    resample_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\resample'
    npz_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\npz'  # npz路径

    for i in trange(len(airway_list)):
        add_label(lobe_list[i], airway_list[i], lobe_airway_path)  # 融合气道树和肺叶
    lobe_airway_list = get_listdir(lobe_airway_path)
    lobe_airway_list.sort()
    for i in trange(len(lobe_airway_list)):
        resample(lobe_airway_list[i], resample_path)  # 将mask重采样到各方向厚度相同, 返回重采样后图像的路径
    resample_list = get_listdir(resample_path)
    resample_list.sort()
    for i in trange(len(resample_list)):
        nii2npz(resample_list[i], npz_path)

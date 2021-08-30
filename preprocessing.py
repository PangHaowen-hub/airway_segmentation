import os
from dcm2nii import dcm_nii
from extract_mimics_airway import extract_mask
from airway_lobe_merge import add_label
from nii_resample import resample
from nii2npz import nii2npz
if __name__ == '__main__':
    main_path = r'D:\my_code\airway_segmentation\1234567'  # 主文件夹，这个病人的所有文件都存到这个文件夹下
    ct_path = r'D:\my_code\airway_segmentation\1234567\airway'  # mimics导出的dicom格式图像，其中保存了气道树分割信息
    lobe_path = r'D:\my_code\airway_segmentation\1234567\lobe_mask.nii.gz'  # 由nnUnet分割得出的肺叶mask
    dcm_nii(ct_path, ct_path + '.nii.gz')  # dicom转为nii
    extract_mask(ct_path + '.nii.gz')  # 从nii中提取气道树，并保存
    lobe_airway_mask_path = os.path.join(main_path, 'lobe_airway_mask.nii.gz')  # 气道树和肺叶融合后mask路径
    add_label(lobe_path, ct_path + '.nii.gz', lobe_airway_mask_path)  # 融合气道树和肺叶
    resample_path = resample(lobe_airway_mask_path)  # 将mask重采样到各方向厚度相同, 返回重采样后图像的路径
    npz_path = os.path.join(main_path, 'model.npz')  # 气道树和肺叶融合后mask路径
    nii2npz(resample_path, npz_path)

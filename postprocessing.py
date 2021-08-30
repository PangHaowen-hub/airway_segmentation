import os
from restore_shape import restore_shape
from nii_restore_spacing import resize_image_itk

if __name__ == '__main__':
    main_path = r'D:\my_code\airway_segmentation\1234567'  # 主文件夹，这个病人的所有文件都存到这个文件夹下
    segments_path = r'D:\my_code\airway_segmentation\1234567\segments.npz'  # Airway stage-34 segments.npz
    model_path = r'D:\my_code\airway_segmentation\1234567\model.npz'
    restore_shape_nii_path = restore_shape(model_path, segments_path,
                                           os.path.join(main_path, 'lobe_airway_mask_resample.nii.gz'))
    save_path = os.path.join(main_path, 'airway_segments_mask.nii.gz')
    resize_image_itk(restore_shape_nii_path, os.path.join(main_path, 'airway.nii.gz'), save_path)

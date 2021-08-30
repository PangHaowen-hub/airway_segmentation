import SimpleITK as sitk


def dcm_nii(ct_path, save_path):
    # 读取CT图像
    ct_reader = sitk.ImageSeriesReader()
    dicom_names = ct_reader.GetGDCMSeriesFileNames(ct_path)
    ct_reader.SetFileNames(dicom_names)
    ct_sitk_img = ct_reader.Execute()
    ct_img_arr = sitk.GetArrayFromImage(ct_sitk_img)

    new_mask_img1 = sitk.GetImageFromArray(ct_img_arr)
    new_mask_img1.SetDirection(ct_sitk_img.GetDirection())
    new_mask_img1.SetOrigin(ct_sitk_img.GetOrigin())
    new_mask_img1.SetSpacing(ct_sitk_img.GetSpacing())
    sitk.WriteImage(new_mask_img1, save_path)


if __name__ == '__main__':
    # 原始数据，不能有中文
    ctdir = r'D:\my_code\airway_segmentation\1234567\airway_dcm'
    save_path = r'D:\my_code\airway_segmentation\1234567\airway_dcm.nii.gz'
    dcm_nii(ctdir, save_path)

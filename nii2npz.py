import numpy as np
import SimpleITK as sitk


def nii2npz(img_path, save_path):
    sitk_img = sitk.ReadImage(img_path)
    img_arr = sitk.GetArrayFromImage(sitk_img)
    img_arr = np.flip(img_arr, axis=0)  # 翻转矩阵以适应airway程序
    np.savez(save_path, img_arr)

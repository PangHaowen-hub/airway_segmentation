import numpy as np
import SimpleITK as sitk
import os

def nii2npz(img_path, save_path):
    sitk_img = sitk.ReadImage(img_path)
    img_arr = sitk.GetArrayFromImage(sitk_img)
    img_arr = np.flip(img_arr, axis=0)  # 翻转矩阵以适应airway程序
    _, fullflname = os.path.split(img_path)
    fullflname = 'model'
    np.savez(os.path.join(save_path, fullflname), img_arr)

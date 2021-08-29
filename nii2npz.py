import numpy as np
import SimpleITK as sitk

sitk_img = sitk.ReadImage(r'.\example_data\my_data\lobe_airway_mask_resample.nii.gz')
img_arr = sitk.GetArrayFromImage(sitk_img)
img_arr = np.flip(img_arr, axis=0)
np.savez(r".\example_data\model.npz", img_arr)


new_mask_img = sitk.GetImageFromArray(img_arr)
new_mask_img.SetSpacing((0.8, 0.8, 0.8))
sitk.WriteImage(new_mask_img, r'.\example_data\model.nii.gz')

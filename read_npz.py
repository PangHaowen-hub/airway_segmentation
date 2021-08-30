import numpy as np
import SimpleITK as sitk


data = np.load(r'new_model.npz')
# x = data['color_mask'].astype(int)
x = data['arr_0'].astype(int)

print(x.shape)

new_mask_img = sitk.GetImageFromArray(x)
new_mask_img.SetSpacing((0.8, 0.8, 0.8))
sitk.WriteImage(new_mask_img, r'new_model.nii.gz')

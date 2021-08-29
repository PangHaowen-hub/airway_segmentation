import numpy as np
import SimpleITK as sitk


data = np.load(r'lobes.npz')
x = data['color_mask'].astype(int)
print(x.shape)

new_mask_img = sitk.GetImageFromArray(x)
new_mask_img.SetSpacing((0.8, 0.8, 0.8))
sitk.WriteImage(new_mask_img, r'color_mask.nii.gz')

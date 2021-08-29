import numpy as np
import SimpleITK as sitk


data = np.load(r'D:\github_code\Airway-master\example_data\model2.npz')
x = data['arr_0'].astype(int)
print(x.shape)

new_mask_img = sitk.GetImageFromArray(x)
new_mask_img.SetSpacing((0.8, 0.8, 0.8))
sitk.WriteImage(new_mask_img, r'D:\github_code\Airway-master\example_data\temp2.nii.gz')

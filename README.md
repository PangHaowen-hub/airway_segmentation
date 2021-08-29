# airway_segmentation
第一步：使用mmimics提取气道树，并导出为dicom

第二步：运行dcm2nii.py将dicom转为nii

第三步：运行mimics_extract_airway.py将气道树mask提取出来

第四步：运行nii_resample.py对图像进行重采样

第五步：运行nii2npz.py将nii转为npz


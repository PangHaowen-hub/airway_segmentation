# Airway segmentation
### 1.图像预处理
step 1：使用mimics提取气道树，并导出为dicom

step 2：运行dcm2nii.py将dicom转为nii

step 3：运行extract_mimics_airway.py将气道树mask提取出来

step 4：运行airway_lobe_merge.py将气道树mask和lobe mask融合

step 5：运行nii_resample.py对mask进行重采样

step 6：运行nii2npz.py将nii转为npz
### 2.分割肺段支气管
step 7: 使用airway分割肺段支气管
### 3.后处理
step 8：使用restore_shape.py将stage34中segments.npz恢复原始shape，并保存为nii格式。

step 9：此时图像shape已恢复，需要运行nii_restore_spacing.py恢复spacing

## 快速使用
step 1：运行preprocessing

step 2：Airway分割肺段支气管

step 3：运行postprocessing
# airway_segmentation
step 1：使用mimics提取气道树，并导出为dicom

step 2：运行dcm2nii.py将dicom转为nii

step 3：运行mimics_extract_airway.py将气道树mask提取出来

step 4：运行airway_lobe_merge.py将气道树mask和lobe mask融合

step 5：运行nii_resample.py对mask进行重采样

step 6：运行nii2npz.py将nii转为npz

step 7: 使用airway分割肺段支气管

step 8：使用read_npz.py将stage34中segments.npz转为nii


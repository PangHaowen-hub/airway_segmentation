import numpy as np
import SimpleITK as sitk
import os
from tqdm import trange


def get_listdir_npz(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.npz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def get_listdir_nii(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def restore_img(model_path, segments_path, img_path, save_path):
    model = np.load(model_path)["arr_0"]  # 分割前npz
    model = model.astype(np.uint8)
    segments_model = np.load(segments_path)["color_mask"]  # 支气管分割后的npz
    segments_model = segments_model.astype(np.uint8)
    # Axis description:
    #      0: top to bottom
    #      1: front to back
    #      2: left to right
    new_model = np.zeros_like(model)
    front_index = []
    back_index = []
    for axis in [0, 1, 2]:
        sums = np.sum(np.sum(model, axis=axis), axis=(axis + 1) % 2)

        # Track all =0 layers from front from that axis
        remove_front_index = 0
        while sums[remove_front_index] == 0:
            remove_front_index += 1

        # Track all =0 layers from back from that axis
        remove_back_index = len(sums) - 1
        while sums[remove_back_index] == 0:
            remove_back_index -= 1

        front_index.append(remove_front_index)
        back_index.append(remove_back_index)
    if front_index[2] == 0:
        front_index[2] += 1
    new_model[front_index[2] - 1:back_index[2] + 2,
    front_index[0] - 1:back_index[0] + 2,
    front_index[1] - 1:back_index[1] + 2] = segments_model

    np.savez(segments_path[:-4] + '_restore_shape.npz', new_model)

    new_model = np.flip(new_model, axis=0)

    reference_img = sitk.ReadImage(img_path)
    new_mask_img = sitk.GetImageFromArray(new_model)
    new_mask_img.SetSpacing((0.8, 0.8, 0.8))
    new_mask_img.SetOrigin(reference_img.GetOrigin())
    new_mask_img.SetDirection(reference_img.GetDirection())

    target_img = sitk.ReadImage(img_path)
    target_Size = target_img.GetSize()  # 目标图像大小  [x,y,z]
    target_Spacing = target_img.GetSpacing()  # 目标的体素块尺寸    [x,y,z]
    target_origin = target_img.GetOrigin()  # 目标的起点 [x,y,z]
    target_direction = target_img.GetDirection()  # 目标的方向 [冠,矢,横]=[z,y,x]
    # itk的方法进行resample
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(new_mask_img)  # 需要重新采样的目标图像
    # 设置目标图像的信息
    resampler.SetSize(target_Size)  # 目标图像大小
    resampler.SetOutputOrigin(target_origin)
    resampler.SetOutputDirection(target_direction)
    resampler.SetOutputSpacing(target_Spacing)
    resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    itk_img_resampled = resampler.Execute(new_mask_img)  # 得到重新采样后的图像
    _, fullflname = os.path.split(img_path)
    sitk.WriteImage(itk_img_resampled, os.path.join(save_path, fullflname))


if __name__ == '__main__':
    segments_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\stage-34'  # 分割支气管得出的npz
    segments_list = []
    for roots, dirs, files in os.walk(segments_path):
        for file in files:
            if file.endswith('segments.npz'):
                print(roots, file)
                segments_list.append(os.path.join(roots, file))
    segments_list.sort()

    model_path = r'F:\segment_registration\Registration\original_image\airway_segmentation\model'  # 分割支气管之前的npz
    model_list = get_listdir_npz(model_path)
    model_list.sort()

    img_path = r'F:\segment_registration\Registration\original_image\imgs'
    img_list = get_listdir_nii(img_path)
    img_list.sort()

    save_path = r'F:\segment_registration\Registration\original_image\bronchi_segmentation\bronchi_segmentation'
    for i in trange(7, len(model_list)):
        restore_img(model_list[i], segments_list[i], img_list[i], save_path)

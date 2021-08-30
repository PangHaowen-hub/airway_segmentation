import numpy as np
import SimpleITK as sitk


def restore_shape(model_path, segments_path, reference_img_path):
    model = np.load(model_path)["arr_0"]  # 分割前npz
    model = model.astype(np.uint8)
    segments_model = np.load(segments_path)["color_mask"]  # 支气管分割后的npz
    segments_model = segments_model.astype(np.uint8)
    # Axis description:
    #      0: top to bottom
    #      1: front to back
    #      2: left to right
    print(model.shape)
    print(segments_model.shape)

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
        temp = list(range(remove_front_index - 1)) + list(range(remove_back_index + 2, len(sums)))
        validation_sums = np.sum(np.sum(model, axis=axis), axis=(axis + 1) % 2)

    new_model[front_index[2] - 1:back_index[2] + 2, front_index[0] - 1:back_index[0] + 2,
    front_index[1] - 1:back_index[1] + 2] = segments_model

    np.savez(segments_path[:-4] + '_restore_shape.npz', new_model)

    new_model = np.flip(new_model, axis=0)
    reference_img = sitk.ReadImage(reference_img_path)
    new_mask_img = sitk.GetImageFromArray(new_model)
    new_mask_img.SetSpacing(reference_img.GetSpacing())
    new_mask_img.SetOrigin(reference_img.GetOrigin())
    new_mask_img.SetDirection(reference_img.GetDirection())
    restore_shape_nii_path = segments_path[:-4] + '_restore_shape.nii.gz'
    sitk.WriteImage(new_mask_img, restore_shape_nii_path)
    return restore_shape_nii_path

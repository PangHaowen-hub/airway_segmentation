import os

file_path = os.path.abspath(r"D:\my_code\airway_segmentation\stage1")
for i in range(67):
    a = "{}".format(i).rjust(7, '0')
    file_name = file_path + "\\" + a
    os.makedirs(file_name)

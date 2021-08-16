import os
import glob

file_list = glob.glob("./output/*")
for file in file_list:
    print("remove：{0}".format(file))
    os.remove(file)
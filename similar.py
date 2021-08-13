#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""feature detection."""

import cv2
import os

#TARGET_FILE = '001'
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/output/'
#IMG_SIZE = (200, 200)
IMG_SIZE = (500, 500)

#target_img_path = IMG_DIR + TARGET_FILE
#target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
#target_img = cv2.resize(target_img, IMG_SIZE)

#bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# detector = cv2.ORB_create()
#detector = cv2.AKAZE_create()
#(target_kp, target_des) = detector.detectAndCompute(target_img, None)

#print('TARGET_FILE: %s' % (TARGET_FILE))

imglist = []
stitchimgs = []
count = 1
files = os.listdir(IMG_DIR)
for file in files:
    #if file == '.DS_Store' or file == TARGET_FILE:
    #    continue
    
    if count < 11:
        # 新規対象画像10枚
        imglist.append("{:0>4}.jpg".format(count))
        count += 1
        continue
    count += 1
    
    # 新規画像を対象にグレースケールとリシェイプ
    print(IMG_DIR+file)
    target_img = cv2.imread(IMG_DIR + file, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, IMG_SIZE)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # detector = cv2.ORB_create()
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    # 新規画像と既存10枚を比較、類似度70以下は差し替え(似てる画像を差し替える)    
    for comp in imglist:
        comparing_img_path = IMG_DIR + comp
        try:
            comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
            comparing_img = cv2.resize(comparing_img, IMG_SIZE)
            (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
            matches = bf.match(target_des, comparing_des)
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)
        except cv2.error:
            ret = 100000

        print(comp, ret)
        if ret < 70:
            imglist.remove(comp)
            imglist.append(file)
            print("{} -> {}".format(comp, file))
            break

    if count > 50 and count % 10 == 0:
        for i in imglist:
            stitchimgs.append(cv2.imread(IMG_DIR + i))
        stitcher = cv2.Stitcher.create(mode = 1)
        (status, stitched) = stitcher.stitch(stitchimgs)
        if status == 0:
        	cv2.imwrite("./stiched/{}.png".format(count), stitched)
        else:
        	print("[INFO] image stitching failed ({})".format(status))

    
    if count % 10 != 0:
        continue
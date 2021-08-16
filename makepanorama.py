import cv2
import os
import glob

#動画からの画像切り出し
def save_frame_range_sec(video_path, start_sec, stop_sec, step_sec, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps
    sec = start_sec

    global imgcount    
    while sec < stop_sec:
        imgcount += 1
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}{:0>4}.{}'.format(dir_path, imgcount, ext), frame)
        else:
            return
        sec += step_sec

#類似画像検索
def similar_image(imgs, newimgs):
    IMG_SIZE = (200, 200)
    for file in newimgs:
        # 新規画像を対象にグレースケールとリシェイプ
        #print(IMG_DIR+file)
        #target_img = cv2.imread(IMG_DIR + file, cv2.IMREAD_GRAYSCALE)
        
        
        target_img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        #target_img = cv2.imread(file)
        target_img = cv2.resize(target_img, IMG_SIZE)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # detector = cv2.ORB_create()
        detector = cv2.AKAZE_create()
        (target_kp, target_des) = detector.detectAndCompute(target_img, None)
    
        # 新規画像と既存10枚を比較、類似度70以下は差し替え(似てる画像を差し替える)    
        for comp in imgs:
            #comparing_img_path = IMG_DIR + comp
            comparing_img_path = comp
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
            if ret < 100:
                imgs.remove(comp)
                imgs.append(file)
                print("{} -> {}".format(comp, file))
                break

#パノラマ画像の作成
def stitch_images(imgs):
    global stitchcount
    #global IMG_DIR
    stitchimgs = []

    for i in imgs:
        #stitchimgs.append(cv2.imread(IMG_DIR + i))
        stitchimgs.append(cv2.imread(i))
    stitcher = cv2.Stitcher.create(mode = 1)
    (status, stitched) = stitcher.stitch(stitchimgs)
    if status == 0:
        stitchcount += 1
        cv2.imwrite("./stitched/{:0>4}.png".format(stitchcount), stitched)
    else:
       	print("[INFO] image stitching failed ({})".format(status))

#画像リストの作成
def make_image_list(imgs):
    file_list = glob.glob("./output/*")
    for file in file_list:
        imgs.append(file)

#不要画像の削除
def delete_images(imgs):
    for file in imgs:
        print("remove：{0}".format(file))
        os.remove(file)  

def main():
    imgs = []  #使用する画像
    allimgs = []  #存在するすべての画像
    newimgs = []  #新規切り出し画像
    StartTime = 0  #動画切り出し開始時間(分割開始)
    EndTime =  120 #動画切り出し強制終了時間
    SplitTime = 1  #1度で何秒分の切り出しを行うか
    NowTime = StartTime + SplitTime  #分割終了時間
    StepTime = 0.1  #切り出し間隔
    IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/output/'  #切り出し画像置き場
    

    #初期画像の切り出し
    save_frame_range_sec('video.mp4', StartTime, NowTime, StepTime, 'output/', '')
    #切り出した初期画像のパスをリストとして保持
    make_image_list(imgs)
    #初期パノラマ画像の作成
    stitch_images(imgs)
    #切り出し地点を一つ進める
    StartTime += SplitTime
    NowTime += SplitTime

    while NowTime <= EndTime:
        newimgs.clear()
        allimgs.clear()
        #新規画像の切り出し
        print("s:{}, e:{}".format(StartTime, EndTime))
        save_frame_range_sec('video.mp4', StartTime, NowTime, StepTime, 'output/', '')
        #現在存在する画像の取得
        make_image_list(allimgs)
        #現在使用画像との重複を除いて新規画像リストを作成
        newimgs = list(set(imgs) ^ set(allimgs))
        #類似画像の差し替え
        similar_image(imgs, newimgs)        
        #不要画像の削除(変数名newimgsはリストの使いまわし)
        newimgs.clear()
        newimgs = list(set(imgs) ^ set(allimgs))
        delete_images(newimgs)
        #パノラマ画像の作成
        stitch_images(imgs)

        print(newimgs)
        print(allimgs)
        print(imgs)

        StartTime += SplitTime
        NowTime += SplitTime

    #作成した画像の削除
    allimgs.clear()
    make_image_list(allimgs)
    delete_images(allimgs)

if __name__ == "__main__":
    stitchcount = 0
    imgcount = 0
    main()
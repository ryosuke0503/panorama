import cv2
import os

def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return

#save_all_frames('data/temp/sample_video.mp4', 'data/temp/result', 'sample_video_img')
#save_all_frames('data/temp/sample_video.mp4', 'data/temp/result_png', 'sample_video_img', 'png')

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
    num = 0
    while sec < stop_sec:
        num += 1
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(
                '{}{:0>4}.{}'.format(
                    dir_path, num, ext
                ),
                frame
            )
        else:
            return
        sec += step_sec

save_frame_range_sec('video.mp4', 30, 50, 0.1, 'output/', '')
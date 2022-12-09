import cv2
from PIL import Image
from moviepy.editor import *
from moviepy.video.fx.all import *
import numpy as np
import argparse
import sys
import os

sys.path.append("..")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--dest_path", type=str, required=True)
    parser.add_argument("--speedup_factor", type=int, default=2)

    opts = parser.parse_args()

    os.makedirs(opts.dest_path, exist_ok=True)

    video_name = opts.video_path.split("/")[-1].split(".")[0]
    video = VideoFileClip(opts.video_path)     # 讀取影片

    video = speedx(video, factor=opts.speedup_factor)          # 2 倍速
    new_video_name = f"{opts.dest_path}/{video_name}_speedup_{opts.speedup_factor}.mp4"
    video.write_videofile(new_video_name, temp_audiofile=f"{video_name}_temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    newVideo = VideoFileClip(new_video_name)
    fps = int(newVideo.fps)
    cap = cv2.VideoCapture(new_video_name)

    filename_count = 0
    ct=0
    while(True):
        ret, frame = cap.read()
        # cv2.imshow('frame.jpg', frame)

        if ct%fps==0:
            frame = Image.fromarray(frame)
            s = str(filename_count)
            frame.save(f"{opts.dest_path}/{s.zfill(6)}.jpg")
            filename_count+=1

        ct+=1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
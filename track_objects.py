import copy
from random import randint

import cv2
import keyboard

from draw import MultiBoxDrawer
from utils import is_end


def main(filename):
    # 動画ファイルsetting
    cap = cv2.VideoCapture(filename)
    bboxes = []
    colors = []
    multiTracker = None
    track_object_flg = False
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    
    if (cap.isOpened()== False):
        print("ビデオファイルを開くとエラーが発生しました")

    while(cap.isOpened()):
        if len(bboxes) == 0:
            track_object_flg = False
            multiTracker = None
        
        ret, frame = cap.read()
        if ret == True:
            
            if track_object_flg:
                # get updated location of objects in subsequent frames
                # multiTrackerの出力は bbox = [x0, y0, width(x1-x0), hight(y1-y0)]
                success, boxes = multiTracker.update(frame)
                print(boxes)
                
                # draw tracked objects
                for i, newbox in enumerate(boxes):
                    p1 = (int(newbox[0]), int(newbox[1]))
                    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
            cv2.imshow("Video", frame)
            
            if keyboard.is_pressed("t"):
                multiboxdrawer = MultiBoxDrawer()
                bboxes = multiboxdrawer.draw(frame)
                print(bboxes)
                track_object_flg = True
                multiTracker = cv2.legacy.MultiTracker_create()
                for bbox in bboxes:
                    # bbox = [x0, y0, x1, y1]
                    bbox = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]
                    # multiTrackerへの追加は bbox = [x0, y0, width(x1-x0), hight(y1-y0)]
                    multiTracker.add(cv2.legacy.TrackerKCF_create(), frame, bbox)
                    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            
            # # 画像表示のため遅延を入れておく
            cv2.waitKey(30)
            # qキーが押されたときbreak
            if keyboard.is_pressed("q"):
                break
            if is_end():
                break
        else:
            break
    # 後始末
    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # https://learnopencv.com/multitracker-multiple-object-tracking-using-opencv-c-python/
    filename = 'sample.mp4'
    main(filename)
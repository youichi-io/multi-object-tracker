import cv2
import keyboard

from utils import is_end


def main(filename):
    # 動画ファイルsetting
    cap = cv2.VideoCapture(filename)

    if (cap.isOpened()== False):
        print("ビデオファイルを開くとエラーが発生しました")

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
            cv2.imshow("Video", frame)
            
            # 画像表示のため遅延を入れておく
            cv2.waitKey(25)
            # qキーが押されたときbreak
            # 右上の×ボタンでwindowが閉じられたとき, Escキーが押されたときbreak
            if keyboard.is_pressed("q") or is_end():
                break
        else:
            break
    # 後始末
    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    filename = 'sample.mp4'
    main(filename)
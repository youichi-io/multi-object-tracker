# 描画したバウンディングボックスの座標情報を取得する
import numpy as np
import cv2
from copy import deepcopy
from random import randint
import keyboard
import time

class MultiBoxDrawer:
    # 参考　https://qiita.com/ryo_ryo/items/973007667c528ef23abb
    def draw(self, img):
        m = MouseEventHandler(img)

        cv2.imshow('Select Rois',img)
        cv2.setMouseCallback ("Select Rois",
                            lambda event, x, y, flags, param:
                            m.mouse_event(event, x, y, flags, param, img))

        while True:
            img = m.clone_img
            cv2.imshow("Select Rois", img)
            k = cv2.waitKey(10)
            if keyboard.is_pressed("space") | keyboard.is_pressed("enter"):
                time.sleep(0.3)
                break

        cv2.destroyWindow("Select Rois")
        # 複数のバウンディングボックスの座標情報をreturn
        return m.ROIRegion

class MouseEventHandler:
    def __init__(self, img):
        self.drawing = False # true if mouse is pressed
        self.ix, self.iy = -1, -1
        self.ROIRegion = []
        self.init_img = deepcopy(img)
        self.clone_img = deepcopy(img)
        self.tmp_img = deepcopy(img)

    def mouse_event(self, event, x, y, flags, param, img):
        if event == cv2.EVENT_LBUTTONDOWN: # 左クリック(押し込み)した瞬間の処理
            self.drawing = True
            self.ix, self.iy = x,y
            self.tmp_img = deepcopy(img)

        elif event == cv2.EVENT_MOUSEMOVE: #ドラッグ中の処理
            if self.drawing == True:
                self.clone_img = deepcopy(self.tmp_img)
                cv2.rectangle(self.clone_img, (self.ix, self.iy), (x, y), (0, 0, 255), 2)

        elif event == cv2.EVENT_LBUTTONUP: # 左クリック(離し)した瞬間の処理
            self.drawing = False
            if self.ix != x and self.iy != y:
                self.ROIRegion.append([min(self.ix, x), min(self.iy, y), abs(x-self.ix), abs(y-self.iy)])

        elif event == cv2.EVENT_RBUTTONDOWN: # 右クリック(離し)した瞬間の処理
            self.ROIRegion = []
            self.clone_img = deepcopy(self.init_img)


if __name__ == "__main__":
    multiboxdrawer = MultiBoxDrawer()
    #スペースキーもしくはエンターキーで画像を閉じる
    # 画像ファイルのパス
    path = 'abc.JPG'
    # 画像読み込み
    img_raw = cv2.imread(path)
    ROIs = multiboxdrawer.draw(img_raw)
    print(ROIs)

    # boxの描画
    for roi in ROIs:
        x1, y1, x2, y2 = roi
        B, G, R = randint(0, 255), randint(0, 255), randint(0, 255)
        cv2.rectangle(img_raw,
                pt1=(x1, y1),
                pt2=(x1+x2, y1+y2),
                color=(B, G, R),
                thickness=3,
                lineType=cv2.LINE_4,
                shift=0)

    while True:
        # boxを描画した画像の表示
        cv2.imshow('img', img_raw)
        k = cv2.waitKey(10)
        # Escキー入力で閉じる
        if keyboard.is_pressed("escape"):
            time.sleep(0.3)
            break

    cv2.destroyAllWindows()

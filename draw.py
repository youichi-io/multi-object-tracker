# 描画したバウンディングボックスの座標情報を取得する
import numpy as np
import cv2
from copy import deepcopy
import keyboard
import time

class MultiBoxDrawer:
    # 参考　https://qiita.com/ryo_ryo/items/973007667c528ef23abb
    def draw(self, img):
        m = MouseEventHandler(img)

        cv2.imshow('img',img)
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback ("img",
                            lambda event, x, y, flags, param:
                            m.mouse_event(event, x, y, flags, param, img))

        while True:
            img = m.clone_img
            cv2.imshow("img", img)
            k = cv2.waitKey(10)
            if keyboard.is_pressed("space") | keyboard.is_pressed("enter"):
                time.sleep(0.3)
                break

        cv2.destroyWindow('img')
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
                self.ROIRegion.append([self.ix, self.iy, x, y])

        elif event == cv2.EVENT_RBUTTONDOWN: # 右クリック(離し)した瞬間の処理
            self.ROIRegion = []
            self.clone_img = deepcopy(self.init_img)

if __name__ == "__main__":
    multiboxdrawer = MultiBoxDrawer()
    #スペースキーもしくはエンターキーで画像を閉じる
    dummy_img = 255 * np.ones((500, 500, 3))
    bboxes = multiboxdrawer.draw(dummy_img)
    print("バウンディングボックスの座標")
    print(bboxes)

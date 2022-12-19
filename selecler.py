from random import randint
import cv2

# 画像ファイルのパス
path = 'abc.JPG'

# 画像読み込み
img_raw = cv2.imread(path)

# 複数領域の指定
ROIs = cv2.selectROIs("Select Rois", img_raw, 0, 0)
cv2.destroyWindow("Select Rois")
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

# boxを描画した画像の表示
cv2.imshow('img', img_raw)
# キー入力で閉じる
cv2.waitKey(0)
cv2.destroyAllWindows()
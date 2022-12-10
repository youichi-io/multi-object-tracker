import cv2

def is_end(window_names=["Video"]):
    return_value = False
    # イメージウインドウの x ボタンを押すか、ESC キー入力で終了処理
    window_property = [cv2.getWindowProperty(window_name, cv2.WINDOW_AUTOSIZE) for window_name in window_names]
    if max(window_property) > 0 or (cv2.waitKey(1) & 0xff == 27):
        return_value = True
    return return_value

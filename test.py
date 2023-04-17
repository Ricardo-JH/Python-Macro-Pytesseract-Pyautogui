from OCR_Detect import OCR
import time




while True:
    psm = int(input('set psm: ')) # 11, 6
    thresh = int(input('set thresh: ')) # 0, -10
    detect = OCR(psm=psm, thresh=thresh)
    time.sleep(1)
    img, words = detect.get_boxes_words('.', thresh)
    print(words)
    detect.show_img(img)
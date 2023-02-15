import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import re


class OCR:
    def __init__(self, psm, thresh):
        self.lang = pytesseract.get_languages()
        self.config = f'--psm {psm} --oem 3'
        self.words_thresh = thresh

    
    def set_wordsThresh(self, thresh):
        self.words_thresh = thresh
        
    
    def read_screen(self):
        img = np.array(ImageGrab.grab())
        img = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2RGB)
        return img


    def show_img(self, img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def get_boxes_letters(self, img):
        height, width, _ = img.shape

        boxes = pytesseract.image_to_boxes(img, config=self.config)

        for box in boxes.splitlines():
            box = box.split(' ')
            img = cv2.rectangle(img, (int(box[1]), height - int (box[2])), (int(box[3]), height - int (box[4])), (0, 255, 0), 2)
        
        # self.show_img(img)
        return img

    
    def get_boxes_words(self, pattern='.', thresh=0):
        self.set_wordsThresh(thresh)
        img = self.read_screen()

        height, width, _ = img.shape
        words = []

        data = pytesseract.image_to_data(img, config=self.config, output_type=pytesseract.Output.DICT)
        # print(data['conf'])

        num_boxes = len(data['text'])

        for i in range(num_boxes):
            word = data['text'][i]
            # print(word)
            if float(data['conf'][i]) > self.words_thresh:
                if re.match(pattern, word):
                    (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                    center_x = int(x + (width / 2))
                    center_y = int(y + (height / 2))
                    

                    img = cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
                    img = cv2.circle(img, (center_x, center_y), 2, (0, 0, 255), 1)
                    
                    img = cv2.putText(img, word, (x, y + height + height), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255), 1, cv2.LINE_AA)
                    
                    words.append((word, center_x, center_y))
        
        # self.show_img(img)
        return img, words

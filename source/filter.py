import objects
import HEADER
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage





class filter:


    image = None
    def __init__(self,data):

        self.image = data.image
        self.data = data

    def startFiler(self,data):# this funcation will manage the others one and return status to the caller
        opencvIMAGE = self.medainFirst()
        self.fillImage(opencvIMAGE)
        #data.filteredImg = opencvIMAGE
        return HEADER.unimplement

    def validation(self):# here we will check the image format, size,acsess
        pass

    def ImageConvertor(self):#here we will filter te image
        pass

    def saveImage(self):#copy the image to get ful control
        pass

    def medainFirst(self):
        col = self.image
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        self.data.bwImage = bw


        # Median

        im_med = ndimage.median_filter(bw, 25)

        new_im = np.abs(bw - im_med)

        new_im[new_im < 90] = 255
        new_im[new_im > 230] = 255

        mask = ((new_im < 230) & (new_im > 90))

        new_im[mask] = 0

        imfile = Image.fromarray(new_im)
        new_im = bw
        self.data.bwImage = new_im
        imfile.save("result_bw2.png")
        img = cv2.imread("result_bw2.png", 1)

        # Average
        kernel = np.ones((10, 10), np.float32) / 100
        dst = cv2.filter2D(img, -1, kernel)

        dst[dst < 240] = 0
        dst[dst > 180] = 255

        cv2.imwrite('average.png', dst)
        return dst#openCV image


    def fillImage(self,im_in):
        th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);

        im_floodfill = im_th.copy()

        h, w = im_th.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        cv2.floodFill(im_floodfill, mask, (0, 0), 255);

        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        im_out = im_th | im_floodfill_inv

        cv2.imwrite("result.png", im_th)
        cv2.imwrite("result2.png", im_floodfill)
        cv2.imwrite("result3.png", im_floodfill_inv)

        im_out =cv2.cvtColor(im_out, cv2.COLOR_BGR2GRAY)
        im_out[im_out<240] = 0
        cv2.imwrite("resultaaa4.png", im_out)
        self.data.filteredImg = im_out

        return im_out





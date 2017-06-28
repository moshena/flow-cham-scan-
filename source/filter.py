import objects
import HEADER
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
from datetime import datetime





class filter:


    image = None
    def __init__(self,data):

        self.image = data.image
        self.data = data

    def startFiler(self,data):# this funcation will manage the others one and return status to the caller
        opencvIMAGE = self.medainFirst()
        #self.fillImage(opencvIMAGE)
        #data.filteredImg = opencvIMAGE
        return HEADER.success

    def medainFirst(self):
        now1 = datetime.now()
        col = self.image
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        self.data.bwImage = bw


        # Median
        """
        to clean the image from big noise like shadow
        Medain cut the noise
        """
        WINDOWS_MEDIAN_SIZE = 5
        im_med_noise = ndimage.median_filter(bw,WINDOWS_MEDIAN_SIZE*WINDOWS_MEDIAN_SIZE) # only nosie

        im_clean = np.abs(bw - im_med_noise)


        """
        make BW image
        """
        im_clean[im_clean < 90] = 255
        im_clean[im_clean > 230] = 255

        mask = ((im_clean < 230) & (im_clean > 90))

        im_clean[mask] = 0

        imfile = Image.fromarray(im_clean)
        self.data.bwImage = im_clean
        imfile.save("trash/result_bw2.png")
        img = cv2.imread("trash/result_bw2.png", 1)

        # Average
        """
        to complete lines that the user didn`t fill we doing average to smear the lines
        Note: this operation smear all the image so it is not usfeull for word rec
        """
        WINDOWS_AVERGAE_SIZE = 6
        denominator = WINDOWS_AVERGAE_SIZE*WINDOWS_AVERGAE_SIZE
        kernel = np.ones((WINDOWS_AVERGAE_SIZE, WINDOWS_AVERGAE_SIZE), np.float32) / denominator
        imageAfterAve = cv2.filter2D(img, -1, kernel)

        cv2.imwrite('trash/NEW2.png', imageAfterAve)

        # strenghten the BLACK color "real data" and replacements the BLACK to be White and the WHITE to be black

        imageAfterAve[imageAfterAve < 240] = 0
        imageAfterAve[imageAfterAve > 180] = 255

        imageAfterAve[imageAfterAve == 255] = 200
        imageAfterAve[imageAfterAve == 0 ] = 255
        imageAfterAve[imageAfterAve == 200] = 0
        now2 = datetime.now()

        print(now2-now1)
        self.data.filteredImg = imageAfterAve# save the average inmage on local storage
        cv2.imwrite('trash/average.png', imageAfterAve)


        return imageAfterAve#openCV image

    def fillImage(self,im_in):
        """

        :param im_in:  im_in image to fill with colse shapes
        :return: openCV format image with full images
        """

        th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);

        im_floodfill = im_th.copy()

        h, w = im_th.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        cv2.floodFill(im_floodfill, mask, (0, 0), 255);

        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        im_out = im_th | im_floodfill_inv

        self.data.filteredImg2 =np.copy(im_out)
        self.data.filteredImg = im_out

        return im_out





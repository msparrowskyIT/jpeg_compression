import numpy as np
import cv2
import processing_image as pi

img = cv2.imread('./images/lena.png', cv2.IMREAD_COLOR )
cv2.imshow('Orginal lena', cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

inv_img = np.stack([pi.process_image(channel, 'Q90') for channel in cv2.split(img)],2)
cv2.imshow('Compresed lena', cv2.cvtColor(inv_img, cv2.COLOR_BGR2GRAY))

cv2.waitKey(0)
cv2.destroyAllWindows()













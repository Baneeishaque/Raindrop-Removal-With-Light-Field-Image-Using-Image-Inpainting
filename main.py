import cv2 as cv
import numpy as np
from scipy import ndimage

# read the image file
depthMapImage = cv.imread('depth_01.png', cv.IMREAD_ANYDEPTH)

# converting to its binary form
ret, bw_img = cv.threshold(depthMapImage, 127, 255, cv.THRESH_BINARY)

cv.imshow("Original Depth Map Iamge", depthMapImage)
cv.imshow("Binary Image of Depth Map Image", bw_img)

kernel = np.ones((5, 5), np.uint8)
closing = cv.morphologyEx(bw_img, cv.MORPH_CLOSE, kernel)
cv.imshow("Binary Image of Depth Map after Closing", closing)

opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
cv.imshow("Binary Image of Depth Map after Closing & Opening", opening)

erosion = cv.erode(opening, kernel, iterations=1)
cv.imshow("Binary Image of Depth Map after Closing, Opening & Erosion", opening)

lightFieldImage = cv.imread('img_01.png')

highPassFilter = np.array([[0, -1, 0],
                           [-1,  5, -1],
                           [0, -1, 1]])

print("Shape of Original Image", lightFieldImage.shape)
print("Shape of High Pass Filter", highPassFilter.shape)
highPassFilter = highPassFilter[:, :, None]  # Add singleton dimension
print("Shape of High Pass Filter", highPassFilter.shape)

highPassFilteredImage = ndimage.convolve(lightFieldImage, highPassFilter)
highPassFilteredImage = highPassFilteredImage.squeeze() # Remove singleton dimension

cv.imshow("Original Image", lightFieldImage)
cv.imshow("High Pass Filtered Image", highPassFilteredImage)

cv.waitKey(0)
cv.destroyAllWindows()

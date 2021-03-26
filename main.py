import cv2 as cv
import numpy as np
from scipy import ndimage

# read the image file
depthMapImage = cv.imread('depth_01.png', cv.IMREAD_ANYDEPTH)

# converting to its binary form
ret, binaryDepthMapImage = cv.threshold(depthMapImage, 127, 255, cv.THRESH_BINARY)

cv.imshow("Original Depth Map Iamge", depthMapImage)
cv.imshow("Binary Image of Depth Map Image", binaryDepthMapImage)

kernel = np.ones((5, 5), np.uint8)
binaryDepthMapImageWithClosing = cv.morphologyEx(binaryDepthMapImage, cv.MORPH_CLOSE, kernel)
cv.imshow("Binary Image of Depth Map after Closing", binaryDepthMapImageWithClosing)

binaryDepthMapImageWithClosingAndOpening = cv.morphologyEx(binaryDepthMapImageWithClosing, cv.MORPH_OPEN, kernel)
cv.imshow("Binary Image of Depth Map after Closing & Opening", binaryDepthMapImageWithClosingAndOpening)

binaryDepthMapImageWithClosingOpeningAndErosion = cv.erode(binaryDepthMapImageWithClosingAndOpening, kernel, iterations=1)
cv.imshow("Binary Image of Depth Map after Closing, Opening & Erosion", binaryDepthMapImageWithClosingOpeningAndErosion)

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

binaryDepthMapImageWithClosingOpeningAndErosionHeight,binaryDepthMapImageWithClosingOpeningAndErosionWidth = binaryDepthMapImageWithClosingOpeningAndErosion.shape[:2]

resizedhighPassFilteredImage=cv.resize(highPassFilteredImage, (binaryDepthMapImageWithClosingOpeningAndErosionWidth,binaryDepthMapImageWithClosingOpeningAndErosionHeight), interpolation = cv.INTER_AREA)
cv.imshow("High Pass Filtered Image after Resize", resizedhighPassFilteredImage)

maskedHighPassFilteredImage = cv.bitwise_and(resizedhighPassFilteredImage, resizedhighPassFilteredImage, mask=binaryDepthMapImageWithClosingOpeningAndErosion)

cv.imshow("Resized High Pass Filtered Image after Masking", maskedHighPassFilteredImage)

cv.waitKey(0)
cv.destroyAllWindows()

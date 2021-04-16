import cv2 as cv
import numpy as np
from scipy import ndimage
from PIL import Image

# Processing Depth Map Image file
# Read the depth map image file
depthMapImage = cv.imread('depth_01.png', cv.IMREAD_ANYDEPTH)

# Converting depth map image to its inverted binary form
ret, invertedBinaryDepthMapImage = cv.threshold(depthMapImage, 127, 255, cv.THRESH_BINARY_INV)

# Show the image with opencv
# cv.imshow("Original Depth Map Image", depthMapImage)
# cv.imshow("Binary Image of Depth Map Image", invertedBinaryDepthMapImage)

# Closing operation on Inverted Binary Image of Depth Map Image
kernel = np.ones((5, 5), np.uint8)
invertedBinaryDepthMapImageWithClosing = cv.morphologyEx(invertedBinaryDepthMapImage, cv.MORPH_CLOSE, kernel)
# cv.imshow("Inverted Binary Image of Depth Map after Closing", invertedBinaryDepthMapImageWithClosing)

# Opening Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingAndOpening = cv.morphologyEx(invertedBinaryDepthMapImageWithClosing,cv.MORPH_OPEN, kernel)
# cv.imshow("Inverted Binary Image of Depth Map after Closing & Opening", invertedBinaryDepthMapImageWithClosingAndOpening)

# Erosion Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosion = cv.erode(invertedBinaryDepthMapImageWithClosingAndOpening, kernel, iterations=1)
# cv.imshow("Inverted Binary Image of Depth Map after Closing, Opening & Erosion", invertedBinaryDepthMapImageWithClosingOpeningAndErosion)

# Processing Original Image
lightFieldImage = cv.imread('img_01.png')

# High Pass Filter
highPassFilter = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 1]])

print("Shape of Original Image", lightFieldImage.shape)
print("Shape of High Pass Filter", highPassFilter.shape)

# Add singleton dimension to High Pass Filter
highPassFilter = highPassFilter[:, :, None]
print("Shape of High Pass Filter", highPassFilter.shape)

# Apply High Pass Filter
highPassFilteredImage = ndimage.convolve(lightFieldImage, highPassFilter)

# Remove singleton dimension
highPassFilteredImage = highPassFilteredImage.squeeze()

# cv.imshow("Original Image", lightFieldImage)
# cv.imshow("High Pass Filtered Image", highPassFilteredImage)

# Resizing High Pass Filtered Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight, invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth = invertedBinaryDepthMapImageWithClosingOpeningAndErosion.shape[:2]

resizedHighPassFilteredImage = cv.resize(highPassFilteredImage, (invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth, invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight),interpolation=cv.INTER_AREA)
# cv.imshow("High Pass Filtered Image after Resize", resizedHighPassFilteredImage)

# Resizing Original Image
resizedOriginalImage = cv.resize(lightFieldImage, (invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth, invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight), interpolation=cv.INTER_AREA)
cv.imshow("Original Image after Resize", resizedOriginalImage)

# Edge Connect
# Image Composite
# Create, Show & Write White Image
# whiteImage = np.zeros([invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight,invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,3], dtype=np.uint8)
# whiteImage.fill(255)
# cv.imwrite('whiteImage.png', whiteImage)
# cv.imshow('White Image',whiteImage)

# Saving Images - Using cv2.imwrite()
cv.imwrite('resizedOriginalImage_01.png', resizedOriginalImage)
cv.imwrite('invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png', invertedBinaryDepthMapImageWithClosingOpeningAndErosion)

# Using Pillow
# White Image
resizedOriginalImagePillow = Image.open('resizedOriginalImage_01.png')
whiteImagePillow = Image.new("1", resizedOriginalImagePillow.size, 255)
# TODO : Bug Fix - Title not showing on image view
# whiteImagePillow.show(title='White Image Pillow')

# Creating Composite Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow = Image.open('invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png')
invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow.show(title='Inverted Binary Depth Map Image With Closing, Opening And Erosion - Pillow')

compositeImage = Image.composite(whiteImagePillow, resizedOriginalImagePillow, invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow)
compositeImage.show(title='Composite Iamge')
compositeImage.save('compositeImage_01.png')

cv.waitKey(0)
cv.destroyAllWindows()

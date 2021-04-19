import cv2
import numpy
from scipy import ndimage
from PIL import Image
from derainnet import test_model

# from derainnet.test_model import test_model

# Processing Depth Map Image file
# Read the depth map image file
depthMapImage = cv2.imread('depth_01.png', cv2.IMREAD_ANYDEPTH)

# Converting depth map image to its inverted binary form
ret, invertedBinaryDepthMapImage = cv2.threshold(depthMapImage, 127, 255, cv2.THRESH_BINARY_INV)

# Show the image with opencv
# cv.imshow("Original Depth Map Image", depthMapImage)
# cv.imshow("Binary Image of Depth Map Image", invertedBinaryDepthMapImage)

# Closing operation on Inverted Binary Image of Depth Map Image
kernel = numpy.ones((5, 5), numpy.uint8)
invertedBinaryDepthMapImageWithClosing = cv2.morphologyEx(invertedBinaryDepthMapImage, cv2.MORPH_CLOSE, kernel)
# cv.imshow("Inverted Binary Image of Depth Map after Closing", invertedBinaryDepthMapImageWithClosing)

# Opening Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingAndOpening = cv2.morphologyEx(invertedBinaryDepthMapImageWithClosing,
                                                                    cv2.MORPH_OPEN, kernel)
# cv.imshow("Inverted Binary Image of Depth Map after Closing & Opening",
# invertedBinaryDepthMapImageWithClosingAndOpening)

# Erosion Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosion = cv2.erode(invertedBinaryDepthMapImageWithClosingAndOpening,
                                                                    kernel, iterations=1)
# cv.imshow("Inverted Binary Image of Depth Map after Closing, Opening & Erosion",
# invertedBinaryDepthMapImageWithClosingOpeningAndErosion)

# Processing Original Image
lightFieldImage = cv2.imread('img_01.png')

# High Pass Filter
highPassFilter = numpy.array([[0, -1, 0],
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
invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight, invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth = invertedBinaryDepthMapImageWithClosingOpeningAndErosion.shape[
                                                                                                                              :2]

resizedHighPassFilteredImage = cv2.resize(highPassFilteredImage, (
    invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,
    invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight), interpolation=cv2.INTER_AREA)
# cv.imshow("High Pass Filtered Image after Resize", resizedHighPassFilteredImage)

# Resizing Original Image
resizedOriginalImage = cv2.resize(lightFieldImage, (invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,
                                                    invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight),
                                  interpolation=cv2.INTER_AREA)
cv2.imshow("Original Image after Resize", resizedOriginalImage)

# Edge Connect Image Composite Create, Show & Write White Image whiteImage = np.zeros([
# invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight,
# invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,3], dtype=np.uint8) whiteImage.fill(255) cv.imwrite(
# 'whiteImage.png', whiteImage) cv.imshow('White Image',whiteImage)

# Saving Images - Using cv2.imwrite()
cv2.imwrite('resizedOriginalImage_01.png', resizedOriginalImage)
cv2.imwrite('invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png',
            invertedBinaryDepthMapImageWithClosingOpeningAndErosion)

# Using Pillow
# White Image
resizedOriginalImagePillow = Image.open('resizedOriginalImage_01.png')
whiteImagePillow = Image.new("1", resizedOriginalImagePillow.size, 255)
# TODO : Bug Fix - Title not showing on image view
# whiteImagePillow.show(title='White Image Pillow')

# Creating Composite Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow = Image.open(
    'invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png')
invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow.show(
    title='Inverted Binary Depth Map Image With Closing, Opening And Erosion - Pillow')

compositeImage = Image.composite(whiteImagePillow, resizedOriginalImagePillow,
                                 invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow)
compositeImage.show(title='Composite Image')
compositeImage.save('compositeImage_01.png')

# Using derainnet
test_model.test_model(image_path='img_01.png', weights_path='derainnet/model/derain_gan/derain_gan.ckpt-100000')

cv2.waitKey(0)
cv2.destroyAllWindows()

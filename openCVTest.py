import cv2 as cv

depthMapImage = cv.imread('depth_01.png', cv.IMREAD_ANYDEPTH)
# cv.imshow("depthMapImage", depthMapImage)

ret, binaryDepthMapImage = cv.threshold(depthMapImage, 127, 255, cv.THRESH_BINARY)
# cv.imshow("binaryDepthMapImage", binaryDepthMapImage)

ret, invertedBinaryDepthMapImage = cv.threshold(depthMapImage, 127, 255, cv.THRESH_BINARY_INV)
cv.imshow("binaryInvertedDepthMapImage", invertedBinaryDepthMapImage)

cv.imwrite("invertedBinaryDepthMapImage_01.png",invertedBinaryDepthMapImage)

cv.waitKey(0)

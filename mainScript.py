import os
import random

from shutil import copyfile

import cv2
import numpy
import torch

from PIL import Image
from scipy import ndimage

from derainnet import test_model
from edge_connect.src.config import Config
from edge_connect.src.edge_connect import EdgeConnect

import GoogleVisionApi
import AzureComputerVision

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Processing Depth Map Image file
# Read the depth map image file
depthMapImage = cv2.imread('depth_01.png', cv2.IMREAD_ANYDEPTH)

# Converting depth map image to its inverted binary form
ret, invertedBinaryDepthMapImage = cv2.threshold(depthMapImage, 127, 255, cv2.THRESH_BINARY_INV)

# Show the image with opencv
# cv2.imshow("Original Depth Map Image", depthMapImage)
cv2.imwrite('originalDepthMapImage_01.png', depthMapImage)
# cv2.imshow("Binary Image of Depth Map Image", invertedBinaryDepthMapImage)
cv2.imwrite('invertedBinaryDepthMapImage_01.png', invertedBinaryDepthMapImage)

# Closing operation on Inverted Binary Image of Depth Map Image
kernel = numpy.ones((5, 5), numpy.uint8)
invertedBinaryDepthMapImageWithClosing = cv2.morphologyEx(invertedBinaryDepthMapImage, cv2.MORPH_CLOSE, kernel)
# cv2.imshow("Inverted Binary Image of Depth Map after Closing", invertedBinaryDepthMapImageWithClosing)
cv2.imwrite('invertedBinaryDepthMapImageWithClosing_01.png', invertedBinaryDepthMapImageWithClosing)

# Opening Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingAndOpening = cv2.morphologyEx(invertedBinaryDepthMapImageWithClosing,
                                                                    cv2.MORPH_OPEN, kernel)
# cv2.imshow("Inverted Binary Image of Depth Map after Closing & Opening",
#            invertedBinaryDepthMapImageWithClosingAndOpening)
cv2.imwrite('invertedBinaryDepthMapImageWithClosingAndOpening_01.png', invertedBinaryDepthMapImageWithClosingAndOpening)

# Erosion Operation on Inverted Binary Image of Depth Map Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosion = cv2.erode(invertedBinaryDepthMapImageWithClosingAndOpening,
                                                                    kernel, iterations=1)
# cv2.imshow("Inverted Binary Image of Depth Map after Closing, Opening & Erosion",
#            invertedBinaryDepthMapImageWithClosingOpeningAndErosion)
cv2.imwrite('invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png',
            invertedBinaryDepthMapImageWithClosingAndOpening)

# Processing Original Image
lightFieldImage = cv2.imread('img_01.png')

# High Pass Filter
highPassFilter = numpy.array([[0, -1, 0],
                              [-1, 5, -1],
                              [0, -1, 1]])

# print("Shape of Original Image", lightFieldImage.shape)
# print("Shape of High Pass Filter", highPassFilter.shape)

# Add singleton dimension to High Pass Filter
highPassFilter = highPassFilter[:, :, None]
# print("Shape of High Pass Filter", highPassFilter.shape)

# Apply High Pass Filter
highPassFilteredImage = ndimage.convolve(lightFieldImage, highPassFilter)

# Remove singleton dimension
highPassFilteredImage = highPassFilteredImage.squeeze()

cv2.imshow("Original Image", lightFieldImage)
# cv2.imshow("High Pass Filtered Image", highPassFilteredImage)
cv2.imwrite('highPassFilteredImage_01.png', highPassFilteredImage)

# Resizing High Pass Filtered Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight, invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth = invertedBinaryDepthMapImageWithClosingOpeningAndErosion.shape[:2]

resizedHighPassFilteredImage = cv2.resize(highPassFilteredImage, (
    invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,
    invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight), interpolation=cv2.INTER_AREA)
# cv2.imshow("High Pass Filtered Image after Resize", resizedHighPassFilteredImage)
cv2.imwrite('resizedHighPassFilteredImage_01.png', resizedHighPassFilteredImage)

# Resizing Original Image
resizedOriginalImage = cv2.resize(lightFieldImage, (invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,
                                                    invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight),
                                  interpolation=cv2.INTER_AREA)
# cv2.imshow("Original Image after Resize", resizedOriginalImage)
cv2.imwrite('resizedOriginalImage_01.png', resizedOriginalImage)

# Edge Connect Image Composite Create, Show & Write White Image 
whiteImage = numpy.zeros([invertedBinaryDepthMapImageWithClosingOpeningAndErosionHeight, invertedBinaryDepthMapImageWithClosingOpeningAndErosionWidth,3], dtype=numpy.uint8)
whiteImage.fill(255) 
cv2.imwrite('whiteImage.png', whiteImage) 
# cv2.imshow('White Image',whiteImage)

# Using Pillow
# White Image
resizedOriginalImagePillow = Image.open('resizedOriginalImage_01.png')
whiteImagePillow = Image.new("1", resizedOriginalImagePillow.size, 255)
whiteImagePillow.save('whiteImagePillow_01.png')
# TODO : Bug Fix - Title not showing on image view
# whiteImagePillow.show(title='White Image Pillow')

# Creating Composite Image
invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow = Image.open(
    'invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png')
# invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow.show(
    # title='Inverted Binary Depth Map Image With Closing, Opening And Erosion - Pillow')

compositeImage = Image.composite(whiteImagePillow, resizedOriginalImagePillow,
                                 invertedBinaryDepthMapImageWithClosingOpeningAndErosionPillow)
# compositeImage.show(title='Composite Image')
compositeImage.save('compositeImage_01.png')

# Using derainnet
# test_model.test_model(image_path='img_01.png', weights_path='derainnet/model/derain_gan/derain_gan.ckpt-100000')
# deRainNetResult = cv2.imread('derain_ret.png')
# cv2.imshow('DeRainNet Result', deRainNetResult)

# Edge Connect
# Default Config. on places2
places2CheckPointsPath = './edge_connect/checkpoints/places2'
config_path = os.path.join(places2CheckPointsPath, 'config.yml')
# create checkpoints path if doesn't exist
if not os.path.exists(places2CheckPointsPath):
    os.makedirs(places2CheckPointsPath)
copyfile('./edge_connect/config.yml.example', config_path)
# load config file
config = Config(config_path)

config.MODE = 2
config.MODEL = 3
config.INPUT_SIZE = 0

config.TEST_FLIST = './compositeImage_01.png'
config.TEST_MASK_FLIST = './invertedBinaryDepthMapImageWithClosingOpeningAndErosion_01.png'
config.RESULTS = './edge_connect/checkpoints/results'

# cuda visible devices
os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(str(e) for e in config.GPU)

# init device
if torch.cuda.is_available():
    config.DEVICE = torch.device("cuda")
    torch.backends.cudnn.benchmark = True  # cudnn auto-tuner
else:
    config.DEVICE = torch.device("cpu")

# set cv2 running threads to 1 (prevents deadlocks with pytorch dataloader)
cv2.setNumThreads(0)

# initialize random seed
torch.manual_seed(config.SEED)
torch.cuda.manual_seed_all(config.SEED)
numpy.random.seed(config.SEED)
random.seed(config.SEED)

# build the model and initialize
model = EdgeConnect(config)
model.load()

print('\nstart testing...\n')
model.test()

edgeConnectResult = cv2.imread('./edge_connect/checkpoints/results/compositeImage_01.png')
cv2.imshow('Edge Connect Result', edgeConnectResult)

cv2.waitKey(0)
cv2.destroyAllWindows()

# print('\n=== Google Cloud Vision API Results : Original Image ===')
# GoogleVisionApi.testGoogleVisionApi('./img_01.png')
# print('\n=== Google Cloud Vision API Results : Derained Image')
# GoogleVisionApi.testGoogleVisionApi('./edge_connect/checkpoints/results/compositeImage_01.png')

print('\n=== Azure Computer Vision Image Analysis Results : Original Image ===')
AzureComputerVision.testAzureComputerVisionImageAnalysisOnLocalImage("img_01.png")
print('\n=== Azure Computer Vision Image Analysis Results : Derained Image ===')
AzureComputerVision.testAzureComputerVisionImageAnalysisOnLocalImage("edge_connect/checkpoints/results/compositeImage_01.png")

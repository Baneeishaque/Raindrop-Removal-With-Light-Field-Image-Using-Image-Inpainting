import imquality.brisque as brisque
import PIL.Image
from collections import defaultdict
from operator import itemgetter
import numpy
from skimage import feature
import cv2
# import warnings filter
from warnings import simplefilter
from scipy import stats

# TODO : Identify & Fix Warnings
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)


def performImageQualityAnalysis(imageFile,externalImageName):
    print('\n====== Image quality Analysis On '+externalImageName+' ======')
    # image-quality package
    brisqueByImageQualityPackage(PIL.Image.open(imageFile),externalImageName)
    # General Methods for Image Quality Analysis
    generalImageQualityAnalysis(imageFile,externalImageName)

def brisqueByImageQualityPackage(pillowImage,externalImageName):
    # https://pypi.org/project/image-quality/
    # Image must be Pillow Image
    print('\n====== Image quality Analysis On '+externalImageName+' using image-quality package ======')

    # run block of code and catch warnings
    # with warnings.catch_warnings():
	#     # ignore all caught warnings
	#     warnings.filterwarnings("ignore")
	#     # execute code that will generate warnings
    #     print('BRISQUE Score Of '+externalImageName+' : '+str(brisque.score(pillowImage)))

    print('BRISQUE Score Of '+externalImageName+' : '+str(brisque.score(pillowImage)))


def generalImageQualityAnalysis(imageFile,externalImageName):
    # https://www.kaggle.com/shivamb/ideas-for-image-features-and-image-quality
    print('\n==== General Image quality Analysis On '+externalImageName+' ======')
    calculateImageDullness(imageFile,externalImageName)
    calculateImageWhiteness(imageFile,externalImageName)
    calculateAveragePixelWidth(imageFile,externalImageName)
    getDominentColor(imageFile,externalImageName)
    getAverageColor(imageFile,externalImageName)
    getBlurrnessScore(imageFile,externalImageName)


def calculateImageDullness(imageFile,externalImageName):
    print('Dullness Score Of '+externalImageName+' : '+str(perform_color_analysis(PIL.Image.open(imageFile),'black')))
    

def perform_color_analysis(pillowImage,flag):
    # Image must be Pillow Image
    # cut the images into two halves as complete average may give bias results
    size = pillowImage.size
    halves = (size[0]/2, size[1]/2)
    im1 = pillowImage.crop((0, 0, size[0], halves[1]))
    im2 = pillowImage.crop((0, halves[1], size[0], size[1]))

    try:
        light_percent1, dark_percent1 = color_analysis(im1)
        light_percent2, dark_percent2 = color_analysis(im2)
    except Exception as e:
        return None

    light_percent = (light_percent1 + light_percent2)/2 
    dark_percent = (dark_percent1 + dark_percent2)/2 
    
    if flag == 'black':
        return dark_percent
    elif flag == 'white':
        return light_percent
    else:
        return None


def color_analysis(img):
    # obtain the color palatte of the image 
    palatte = defaultdict(int)
    for pixel in img.getdata():
        palatte[pixel] += 1
    
    # sort the colors present in the image 
    sorted_x = sorted(palatte.items(), key=itemgetter(1), reverse = True)
    light_shade, dark_shade, shade_count, pixel_limit = 0, 0, 0, 25
    for i, x in enumerate(sorted_x[:pixel_limit]):
        if all(xx <= 20 for xx in x[0][:3]): ## dull : too much darkness 
            dark_shade += x[1]
        if all(xx >= 240 for xx in x[0][:3]): ## bright : too much whiteness 
            light_shade += x[1]
        shade_count += x[1]
        
    light_percent = round((float(light_shade)/shade_count)*100, 2)
    dark_percent = round((float(dark_shade)/shade_count)*100, 2)
    return light_percent, dark_percent


def calculateImageWhiteness(imageFile,externalImageName):
    print('Whiteness Score Of '+externalImageName+' : '+str(perform_color_analysis(PIL.Image.open(imageFile),'white')))


def calculateAveragePixelWidth(imageFile,externalImageName):
    print('Average Pixel Width Of '+externalImageName+' : '+str(average_pixel_width(PIL.Image.open(imageFile))))


def average_pixel_width(pillowImage):
    # Image must be Pillow Image
    im_array = numpy.asarray(pillowImage.convert(mode='L'))
    edges_sigma1 = feature.canny(im_array, sigma=3)
    apw = (float(numpy.sum(edges_sigma1)) / (pillowImage.size[0]*pillowImage.size[1]))
    return apw*100


def getDominentColor(imageFile,externalImageName):
    print('Dominent Color Of '+externalImageName+' : '+str(get_dominant_color(cv2.imread(imageFile))))


def get_dominant_color(openCvImage):
    # Image must be OpenCV Image
    arr = numpy.float32(openCvImage)
    pixels = arr.reshape((-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

    palette = numpy.uint8(centroids)
    quantized = palette[labels.flatten()]
    quantized = quantized.reshape(openCvImage.shape)

    dominant_color = palette[numpy.argmax(stats.itemfreq(labels)[:, -1])]
    return dominant_color


def getAverageColor(imageFile,externalImageName):
    print('Average Color Of '+externalImageName+' : '+str(get_average_color(cv2.imread(imageFile))))


def get_average_color(openCvImage):
    # Image must be OpenCV Image
    average_color = [openCvImage[:, :, i].mean() for i in range(openCvImage.shape[-1])]
    return average_color


def getBlurrnessScore(imageFile,externalImageName):
    print('Blurrness Score Of '+externalImageName+' : '+str(get_blurrness_score(cv2.imread(imageFile))))


def get_blurrness_score(openCvImage):
    # Image must be OpenCV Image
    image = cv2.cvtColor(openCvImage, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(image, cv2.CV_64F).var()
    return fm


if __name__ == "__main__":
    performImageQualityAnalysis('img_01.png','Original Image')

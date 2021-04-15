from PIL import Image, ImageOps

depthImage = Image.open('depth_01.png')
depthImage.show()

depthImageGray = ImageOps.grayscale(depthImage)
depthImageGray.show()

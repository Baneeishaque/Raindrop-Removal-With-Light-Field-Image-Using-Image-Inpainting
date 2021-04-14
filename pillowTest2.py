from PIL import Image, ImageOps

depthImagePillow = Image.open('invertedBinaryDepthMapImage_01.png')
depthImagePillow.show()

resizedOriginalImagePillow = Image.open('resizedOriginalImage_01.png')
# resizedOriginalImagePillow.show()

whiteImagePillow = Image.new("1", resizedOriginalImagePillow.size, 255)
# whiteImagePillow.show()

compositeImage = Image.composite(whiteImagePillow, resizedOriginalImagePillow, depthImagePillow)
compositeImage.show()

compositeImage.save('compositeImage_01.png')

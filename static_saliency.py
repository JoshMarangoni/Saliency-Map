import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True, help="Path to input image")
ap.add_argument("--save", required=True, help="Path to saved image directory")
args = vars(ap.parse_args())

def resize(img): 
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def saveToDisk(img, imgName): 
    print(imgName)
    path = args["save"] + '/' + imgName + '.jpg'
    print(path)
    cv2.imwrite(path, img)

image = cv2.imread(args["image"])

#saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
saliency = cv2.saliency.StaticSaliencyFineGrained_create()
(success, saliencyMap) = saliency.computeSaliency(image)
saliencyMap = (saliencyMap * 255).astype("uint8")

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

image = resize(image)
cv2.imshow("Image", image)

saliencyMap = resize(saliencyMap)
saveToDisk(saliencyMap, "saliencyMap")
cv2.imshow("Output", saliencyMap)

threshMap = resize(threshMap)
saveToDisk(threshMap, "threshMap")
cv2.imshow("Thresh", threshMap)
cv2.waitKey(0)

import argparse
import cv2

def resize(img): 
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True, help="Path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

#saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
saliency = cv2.saliency.StaticSaliencyFineGrained_create()
(success, saliencyMap) = saliency.computeSaliency(image)
saliencyMap = (saliencyMap * 255).astype("uint8")

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cv2.imshow("Image", resize(image))
cv2.imshow("Output", resize(saliencyMap))
cv2.imshow("Thresh", resize(threshMap))
cv2.waitKey(0)

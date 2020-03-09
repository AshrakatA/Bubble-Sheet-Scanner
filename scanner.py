import cv2
import numpy as np
imref = cv2.imread("test_sample6.jpg",cv2.COLOR_BGR2GRAY)
im = cv2.imread("test_sample9.jpg",cv2.COLOR_BGR2GRAY)

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

def alignImages(im1, im2):
    # Detect ORB features and compute descriptors
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2, None)
	# Match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
	# Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
	# Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]
	# Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)
	# Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
	# Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


def XandY(img):
    #Convert image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#find connected components
    connectivity=4
    ret, thresh2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    Coordinates = cv2.connectedComponentsWithStats(thresh2, connectivity, cv2.CV_32S)
    AnswerCoordinates = Coordinates[3]
	#number of matrix
    XandYLabels = 1
    for center in AnswerCoordinates:
	    #Determine X and Y
        y = center[1]
        x = center[0]
		#print x and y of each answer
        cv2.putText(img,'('+ str(int(x))+','+str(int(y))+')', (int(center[0] + 7), int(center[1] - 3)), cv2.FONT_ITALIC, 0.25,
                    255, 1)
        XandYLabels += 1
    cv2.imshow('Coordinates', img)

    cv2.waitKey(0)


def resize(img):
    scale_percent = 60  # percent of original size
    width = int(1654 * scale_percent / 130) #width of the new img
    height = int(2338 * scale_percent / 200) #height of the new img
    dim = (width, height) # set width and height to dim
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

def answers(img):
    #setting Structuring element to erode and dilate
    SE4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    SE5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
	#Thresholding to make it binary image with black and white
    ret,img = cv2.threshold(img,90,255,cv2.THRESH_BINARY)
	#erode and dilate to remove anyhing but answers
    img_erosion = cv2.erode(img, SE4, iterations=1)
    img_dilation = cv2.dilate(img_erosion, SE5, iterations=1)
    ret, thresh = cv2.threshold(img_dilation, 127, 255, 0)
    answers = cv2.erode(thresh, SE5, iterations=1)
    ret, thresh2 = cv2.threshold(answers, 90, 255, cv2.THRESH_BINARY_INV)
    return thresh2

######################################################################################
imReg, h = alignImages(im, imref)
resized=resize(imReg)
answer=answers(resized)
#######################################################################################

def countCircles(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(img, (3, 3))
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 10, param1=20,param2=10, minRadius=3, maxRadius=10)
    if circles is not None:

        Count_circle = np.uint16(np.around(circles))
        count=1
        Count_circle = sorted(Count_circle[0], key=lambda x: [x[1], x[0]], reverse=False)
        for pt in Count_circle:
            a, b, r = pt[0], pt[1], pt[2]
            cv2.circle(img, (a, b), r, (255, 0, 0), 2)
            cv2.putText(img, str(count), (a+10, b+5), cv2.FONT_ITALIC, 0.6, (255, 0, 0), lineType=cv2.LINE_AA)
            count+=1
       # cv2.imshow("Count Circles", img)
       # cv2.waitKey(0)
        return Count_circle
#cv2.imshow("Original", resize(im))
#cv2.imshow("resized", resized)
#cv2.imshow("answers", answer)
#XandY(answer)
#cv2.imshow("answers", answer)
#countCircles(answer)
#cv2.waitKey(0)
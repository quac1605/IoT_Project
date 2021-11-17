import numpy as np 
import cv2
import matplotlib.pyplot as plt
def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]
#import piture
frame = cv2.imread('./line.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

cv2.imshow("Detect frame",hsv)

#define white range
<<<<<<< HEAD
lower_white = np.array([0,0,0])
upper_white = np.array([10,10,255])
=======
lower_white = np.array([15,40,40])
upper_white = np.array([15,255,255])
>>>>>>> a1cbb67e32412de02b57dc4c38fb8aaf45e54243

#mask erstellen
mask = cv2.inRange(hsv,lower_white,upper_white)
cv2.imshow("Detect mask",mask)

#detection edges of lines
edges = cv2.Canny(mask, 200, 400)


#cutting image
height,width = edges.shape
mask = np.zeros_like(edges) #Return an array of zeros with the same shape and type as a given array

polygon = np.array([[
	(0,height * 1/2),
	(width,height * 1/2),
	(width,height),
	(0,height),
	]],np.int32)

cv2.fillPoly(mask, pts = [polygon], color=(255,255,255))
cropped_edges = cv2.bitwise_and(edges, mask)
cv2.imshow("Detect edges",cropped_edges)

#detect line segment
rho = 1  # distance precision in pixel, i.e. 1 pixel
angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
min_threshold = 10  # minimal of votes
line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, #output: only points
                                    np.array([]), minLineLength=8, maxLineGap=4)

#drawing line
lane_lines = []

height, width, _ = frame.shape
left_fit = []
right_fit = []

boundary = 1/3
left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

for line_segment in line_segments:
    for x1, y1, x2, y2 in line_segment:
        if x1 == x2:
            logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
            continue
        fit = np.polyfit((x1, x2), (y1, y2), 1)
        slope = fit[0]
        intercept = fit[1]
        if slope < 0:
            if x1 < left_region_boundary and x2 < left_region_boundary:
            	left_fit.append((slope, intercept))
        else:
            if x1 > right_region_boundary and x2 > right_region_boundary:
                right_fit.append((slope, intercept))

left_fit_average = np.average(left_fit, axis=0)
if len(left_fit) > 0:
	lane_lines.append(make_points(frame, left_fit_average))

<<<<<<< HEAD
right_fit_average = np.average(right_fit, axis=0)
if len(right_fit) > 0:
    lane_lines.append(make_points(frame, right_fit_average))

<<<<<<< HEAD
=======
logging.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]
cv2.imshow("Input",lane_lines)
#cv2.imshow("Input",cropped_edges)
=======
#ok ok
>>>>>>> a1cbb67e32412de02b57dc4c38fb8aaf45e54243
cv2.imshow("Input",cropped_edges)
>>>>>>> 4298bdbcec053ec2f1737962dcefe023539a8bdc
cv2.waitKey(0)
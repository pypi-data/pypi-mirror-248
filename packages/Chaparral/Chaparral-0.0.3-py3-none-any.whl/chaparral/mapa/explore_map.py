import cv2 as cv
import numpy as np

# read image
main_path = 'data/Mapa General Campo Chichimene.png'
pozos_path = 'data/clusters_prv.png'
via1_path = 'data/pavimentada_prv.png'
via2_path = 'data/pavimentada_angosta_prv.png'

img_main = cv.imread(main_path)
img_pozos = cv.imread(pozos_path)
img_via1 = cv.imread(via1_path)
img_via2 = cv.imread(via2_path)
# crop = img[1210:1225, 6995:7015]  # pozo
# crop = img[1900:2500, 8710:8750]  # vias

hsv_pozos = cv.cvtColor(img_pozos, cv.COLOR_BGR2HSV)
hsv_via1 = cv.cvtColor(img_via1, cv.COLOR_BGR2HSV)
hsv_via2 = cv.cvtColor(img_via2, cv.COLOR_BGR2HSV)

# mask color #00FF00 Green1
pozo_mask = cv.inRange(hsv_pozos, (45, 195, 245), (48, 198, 252))
via1_mask = cv.inRange(hsv_via1, (45, 195, 245), (48, 198, 252))
via2_mask = cv.inRange(hsv_via2, (45, 195, 245), (48, 198, 252))

# dilatation_size = 5
# dilation_shape = cv.MORPH_ELLIPSE
# element = cv.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
#                                     (dilatation_size, dilatation_size))
# pozo_mask = cv.erode(pozo_mask, element)
# pozo_mask = cv.dilate(pozo_mask, element)
#
# contours, _ = cv.findContours(pozo_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# # cv.drawContours(mask, contours, -1, 255, 30)
# font = cv.FONT_HERSHEY_SIMPLEX
#
# for i, c in enumerate(contours):
#     x, y = c.mean(axis=0)[0]
#     cv.circle(img, (int(x), int(y)), 25, (0, 0, 0), -1)
#     cv.putText(img, str(i),
#                (int(x + 50), int(y + 50)),
#                font, 5, (0, 0, 0), 10, cv.FILLED)

# show processed image
cv.imshow('map', via2_mask + via1_mask)
cv.waitKey(0)

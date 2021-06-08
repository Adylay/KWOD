
import numpy
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from cv2 import MORPH_ELLIPSE
from scipy import ndimage
from skimage import color
from skimage import io
from skimage.restoration import denoise_nl_means
import cv2


def stenosis(image_filename):

    img = mpimg.imread(image_filename, 0)
    gray = color.rgb2gray(img)
    # plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
    # plt.show()

    norm = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    blur = cv2.bilateralFilter(norm,9,75,75)

    denoise = denoise_nl_means(blur, 6, 9, 0.08, multichannel=True, fast_mode = False)

    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cl1 = clahe.apply(gray_image)
    # plt.imshow(cl1, cmap=plt.get_cmap('gray'))
    # plt.show()

    # Taking a matrix of size 3 as the kernel
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    img_erosion = cv2.erode(cl1, kernel1, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel1, iterations=1)
    img_dilation = cv2.dilate(img_dilation, kernel1, iterations=1)
    img_erosion = cv2.erode(img_dilation, kernel1, iterations=1)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
    img_erosion = cv2.erode(img_erosion, kernel2, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel2, iterations=1)
    img_dilation = cv2.dilate(img_dilation, kernel2, iterations=1)
    img_erosion = cv2.erode(img_dilation, kernel2, iterations=1)

    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (80, 80))
    img_erosion = cv2.erode(img_erosion, kernel3, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel3, iterations=1)
    img_dilation = cv2.dilate(img_dilation, kernel3, iterations=1)
    img_erosion = cv2.erode(img_dilation, kernel3, iterations=1)
    # plt.imshow(img_erosion, cmap=plt.get_cmap('gray'))
    # plt.show()

    img3 = img_erosion-cl1
    #gray_img3 = color.rgb2gray(img3)
    # plt.imshow(img3, cmap=plt.get_cmap('gray'))
    # plt.show()

    th, im_gray_th_otsu = cv2.threshold(img3, 0, 1, cv2.THRESH_OTSU)
    # plt.imshow(im_gray_th_otsu, cmap=plt.get_cmap('gray'))
    # plt.show()
    # print(im_gray_th_otsu)

    im_gray_th_otsu = 1-im_gray_th_otsu

    ret, labels = cv2.connectedComponents(im_gray_th_otsu)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0

    # plt.subplot(222)
    # plt.title('Objects counted:'+ str(ret-1))
    # plt.imshow(labeled_img)
    # # print('objects number is:', ret-1)
    # # print(labels)
    # plt.show()

    counts, bins = np.histogram(labels, bins=range(0, ret-1))
    # print(counts)
    sorted_v = sorted(counts, reverse=True)
    # print(sorted_v)
    # print(bins[np.where(counts == sorted_v[1])])

    labels[labels != bins[np.where(counts == sorted_v[1])]] = 0
    labels[labels == bins[np.where(counts == sorted_v[1])]] = 1

    # plt.imshow(labels, cmap=plt.get_cmap('gray'))
    # plt.show()
    # # print(numpy.amax(labels))

    kernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    c = labels.astype('uint8')
    label_dilation = cv2.morphologyEx(c, cv2.MORPH_CLOSE, kernel4)
    # plt.imshow(label_dilation, cmap=plt.get_cmap('gray'))
    # plt.show()

    distanse_transform = ndimage.distance_transform_edt(label_dilation)

    norm_dist = cv2.normalize(distanse_transform, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # plt.imshow(distanse_transform, cmap=plt.get_cmap('gray'))
    # plt.show()

    label_dilation = label_dilation*255;
    thinned = cv2.ximgproc.thinning(label_dilation, cv2.ximgproc.THINNING_ZHANGSUEN)
    thinned = cv2.normalize(thinned, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    [r,c] = numpy.shape(thinned)
    thinned = thinned[1:r-1, 1:c-1]
    # plt.imshow(thinned, cmap=plt.get_cmap('gray'))
    # plt.show()

    norm_dist = norm_dist[1:r-1, 1:c-1]
    #

    dist = norm_dist*thinned;
    # plt.imshow(dist, cmap=plt.get_cmap('gray'))
    # plt.show()

    sortDist = dist[dist != 0]


    min = numpy.amin(sortDist)
    max = numpy.amax(sortDist)
    przewezenie = (max-min)*100/max
    print(max)
    print(min)
    print(przewezenie)

    return min, max, przewezenie, label_dilation
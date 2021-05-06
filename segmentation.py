def segmentation (img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min):
    import cv2 as cv
    import numpy as np
    from number import number
# PROGOWANIE ___________________________________________________________________________________________________________
    img_bin = cv.adaptiveThreshold(img_gray_filtr, thresh, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, fg_tresh_max, fg_tresh_min)
    img_bin_bg = cv.adaptiveThreshold(img_gray_filtr, thresh, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, bg_tresh_max, bg_tresh_min)


# MORFOLOGIA ___________________________________________________________________________________________________________
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    kernel_d = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    kernel_e = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))

    maska_fg_true = cv.dilate(img_bin, kernel_d, iterations=4)
    sure_fg = cv.erode(maska_fg_true, kernel_e, iterations=3)
    sure_fg = np.uint8(sure_fg)

    maska_bg_true = cv.erode(img_bin_bg, kernel_d, iterations=1)
    sure_bg = cv.dilate(maska_bg_true, kernel, iterations=7)

# WATHERSHED ___________________________________________________________________________________________________________
    unknown = cv.subtract(sure_bg, sure_fg)

    _, markers = cv.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown == 255] = 0

    img_color = cv.cvtColor(img_gray_filtr, cv.COLOR_GRAY2BGR)

    edges = cv.watershed(img_color, markers)

# WYBIERANIE NACZYNIA __________________________________________________________________________________________________
    seed = np.copy(img_gray_filtr)
    seed[:, :] = [0]
    number_img = number(edges+1)

    seed[edges == 2] = 1

# ################################################ KONIEC SEGMENTACJI ################################################ #
    return seed
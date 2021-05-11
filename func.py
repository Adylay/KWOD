def imadjust(snc, a, b, c, d, gamma=1):
    img_rows, img_cols = snc.shape
    y = snc
    for i in range(img_cols):
        for j in range(img_rows):
            if snc[j, i] <= a:
                y[j, i] = c
            elif snc[j, i] >= b:
                y[j, i] = d
            else:
                y[j, i] = int((((snc[j, i] - a) / (b - a)) ** gamma) * (d - c) + c)

    return y


import numpy as np



def number(snc):
    img_rows, img_cols = snc.shape
    max_img = snc.max()
    min_img = snc.min()
    num_vec = np.zeros(max_img+1)
    for i in range(img_cols):
        for j in range(img_rows):
            pom = snc[i, j]
            if pom != 2:
                num_vec[pom] = num_vec[pom]+1
    num = 0
    max_value = num_vec.max()
    for i in range(max_img+1):
        if num_vec[i] == max_value:
            num = i

    return num



def preprocesing(path, down_tresh, up_thresh, left_tresh, right_tresh, gamma):

    import cv2 as cv
    # from imadjust import imadjust

# ################################################# WCZYTANIE OBRAZU ################################################# #
    img_gray = cv.imread(path, 0)

# ######################################## PRZYGOTOWANIE DO SEGMENTACJI ############################################## #

# FILTRACJA ____________________________________________________________________________________________________________
    img_gray_filtr = cv.medianBlur(img_gray, 5)

# WYROWNANIE HISTOGRAMU ________________________________________________________________________________________________
    clahe = cv.createCLAHE(clipLimit=1., tileGridSize=(3, 3))
    img_gray_equal = clahe.apply(img_gray_filtr)

# NIELINIOWA ZMIANA JASNOSCI ___________________________________________________________________________________________
    img_gamma = imadjust(img_gray_equal, down_tresh, up_thresh, 10, 215, gamma)

# ########################################## KONIEC PRZYGOTOWANIA DO SEGMENTACJI ##################################### #
    return img_gamma


def segmentation (img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min):
    import cv2 as cv
    import numpy as np
    # from number import number
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
def preprocesing(path, down_tresh, up_thresh, left_tresh, right_tresh, gamma):

    import cv2 as cv
    from imadjust import imadjust

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
'''
Projekt w ramach przedmiotu Komputerowe Wspomaganie Obrazowej Diadnostyki Medycznej
wykrywanie przeweżen w tetnicach wieńcowych
'''

# ############################################## BIBLIOTEKI ########################################################## #
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy import ndimage
import pandas as pd
from skimage.morphology import skeletonize
from skimage import data
from skimage.util import invert

# ############################################### FUNKCJE WLASNE ##################################################### #
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

# ############################################## WCZYTYWANIE OBRAZÓW ################################################# #
img_gray = cv.imread('Image_3', 0)

plt.imshow(img_gray,'gray')
plt.show()

print(@)
# ######################################## PRZYGOTOWANIE DO SEGMENTACJI ############################################## #
'''
# FILTRACJA ____________________________________________________________________________________________________________
img_gray_filtr = cv.medianBlur(img_gray, 5)

# WYROWNANIE HISTOGRAMU ________________________________________________________________________________________________
clahe = cv.createCLAHE(clipLimit=1., tileGridSize=(3, 3))
img_gray_equal = clahe.apply(img_gray_filtr)


# NIELINIOWA ZMIANA JASNOSCI ___________________________________________________________________________________________
down_tresh = 0
up_thresh = 180
gamma = 1.2
img_gamma = imadjust(img_gray_equal, down_tresh, up_thresh, 10, 255, gamma)


# ########################################## KONIEC PRZYGOTOWANIA DO SEGMENTACJI ##################################### #


# ###################################################### SEGMENTACJA ################################################# #

# PROGOWANIE ___________________________________________________________________________________________________________
thresh = 100
img_bin = cv.adaptiveThreshold(img_gray_filtr, thresh, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 7)
img_bin_bg = cv.adaptiveThreshold(img_gray_filtr, thresh, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 31, 11)

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

seed[edges == 3] = 1
plt.imshow(sure_fg)
plt.show()


# ################################################ KONIEC SEGMENTACJI ################################################ #


# ############################################## PRZETWRARZANIE MASKI ################################################ #

# DOCINANIE MASKI ______________________________________________________________________________________________________
cut_vertical = 20
cut_horizonatal = 70

cut = seed[cut_horizonatal:-cut_horizonatal, cut_vertical:-cut_vertical]
# cut_dilate = cv.dilate(cut, kernel_d, iterations=1)

# MASKA O WIELKOSCI ORGINALNEGO ________________________________________________________________________________________
img_good_binary = np.copy(img_gray)
img_good_binary[:, :] = [0]

img_rows, img_cols = cut.shape  # rozmiar obrazu
xp = cut_horizonatal
xk = img_rows+cut_horizonatal
yp = cut_vertical
yk = img_cols+cut_vertical

img_good_binary[xp:xk, yp:yk] = cut
plt.subplot(1, 2, 1)
plt.imshow(img_gray, 'gray')

plt.subplot(1, 2, 2)
plt.title("img_good_binary")
plt.imshow(img_good_binary, 'gray')
plt.show()
print(img_good_binary.max())
# ############################################ KONIEC PRZETWARZANIA MASKI ############################################ #

# ZAPIS ZDJECIA ________________________________________________________________________________________________________
cv.imwrite('outt.png', img_good_binary*255)

# SZKIELET NACZYN WIENCOWYCH ___________________________________________________________________________________________
skeleton = skeletonize(img_good_binary)

# WYKRYWANIE KRAWEDZI __________________________________________________________________________________________________

out_canny = cv.Canny(img_gray, 10, 80)



laplacian = np.array(([1, 1, 1],
                      [1, -8, 1],
                      [1, 1, 1]), dtype=np.float32)*30

img_laplace = cv.filter2D(img_gamma_filtr, -1, laplacian)

kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))

img_erode = cv.erode(img_laplace, kernel, iterations=1)
img_dilate = cv.dilate(img_erode, kernel, iterations=4)
img_erode = cv.erode(img_dilate, kernel, iterations=3)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
img_dilate = cv.dilate(img_erode, kernel, iterations=2)
img_erode = cv.erode(img_dilate, kernel, iterations=2)


# WYCIECIE ORGINALNYCH NACZYN __________________________________________________________________________________________
img_bitwise = cv.bitwise_and(img_gray_filtr, img_gray_filtr, mask=img_good_binary)

# WYSWIETLANIE SZKIELETU _______________________________________________________________________________________________
img_bitwise_color = cv.cvtColor(img_bitwise, cv.COLOR_GRAY2BGR)
img_bitwise_color[skeleton == 1] = [255, 0, 0]
img_color[skeleton == 1] = [255, 0, 0]
cv.imwrite('out_skiel1.png', img_bitwise_color)
cv.imwrite('out_skiel1.png', img_color)


plt.title("img_bitwise")
plt.imshow(img_color, interpolation="bicubic")
plt.show()

'''

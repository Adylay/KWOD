import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy import ndimage
import pandas as pd
from skimage.morphology import skeletonize
from skimage import data

from preprocesing import preprocesing

path = 'Image_1.png'
down_tresh = 0
up_thresh = 220
left_tresh = 10
right_tresh = 215
gamma = 1.2

preprocesing(path, down_tresh, up_thresh, left_tresh, right_tresh, gamma)

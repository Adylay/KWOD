import tkinter as tk
from tkinter import filedialog, Text
from tkinter.filedialog import askopenfile
import os
from PIL import Image, ImageTk
from functions import resize_image, display_images
from tkinter import ttk
from matplotlib import pyplot as plt
from scipy import ndimage

from func import *


def next_tab(ntab):
    tabControl.select(ntab + 1)


def print_val(var):
    print(var)


def reset_prep(label, button):
    label.destroy()
    button.forget()

def reset_label(label):
    label.destroy()


def prep_img(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma):
    global img_gamma
    down_tresh = down_tresh.get()
    up_tresh = up_tresh.get()
    left_tresh = left_tresh.get()
    right_tresh = right_tresh.get()
    gamma = gamma.get()

    img_gamma = preprocesing(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma)

    img_pil = Image.fromarray(img_gamma, "L")

    img_gm = ImageTk.PhotoImage(img_pil)
    global img_label2
    img_label2 = tk.Label(tab_prep, image=img_gm, bg="white")
    img_label2.image = img_gm
    img_label2.pack(side=tk.LEFT, padx=50)
    tab_prep.update_idletasks()

    global n_seg_btn
    n_seg_btn = tk.Button(tab_prep, text=">> Segmentacja", command=lambda: next_tab(1), font=("Raleway", 13),
                          bg="white")
    n_seg_btn.pack(side=tk.BOTTOM, padx=15, pady=15)

    print(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma)

    rst_btn = tk.Button(param_prep, text="Reset", command=lambda: reset_prep(img_label2, n_seg_btn),
                        font=("Raleway", 13),
                        bg="white")
    rst_btn.grid(row=7, column=1, pady=15)


def seg_img(img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min):
    thresh = thresh.get()
    fg_tresh_max = fg_tresh_max.get()
    fg_tresh_min = fg_tresh_min.get()
    bg_tresh_max = bg_tresh_max.get()
    bg_tresh_min = bg_tresh_min.get()

    img_seg = segmentation(img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min)
    img_seg2 = img_seg * 250
    img_pil = Image.fromarray(img_seg2, "L")
    img_sgm = ImageTk.PhotoImage(img_pil)
    img_label3 = tk.Label(tab_seg, image=img_sgm, bg="white")
    img_label3.image = img_sgm
    img_label3.pack(side=tk.LEFT, padx=50)

    print(thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min)
    rst_btn2 = tk.Button(param_seg, text="Reset", command=lambda: reset_label(img_label3), font=("Raleway", 13),
                         bg="white")
    rst_btn2.grid(row=7, column=1, pady=15)


flag = False
global img_gm
root = tk.Tk()
root.title('Aplikacja do segmentacji tętnic wieńcowych')
root.iconbitmap('icon1.ico')
root.geometry('800x600+%d+%d' % (100, 10))  # place GUI at x=350, y=10

tabControl = ttk.Notebook(root)
# tabControl.grid(columnspan=4, rowspan=4, row=0)
tabControl.pack(fill="both", expand=1)

tab_start = tk.Frame(tabControl, width=800, height=600, bg="#20bebe")
tab_prep = tk.Frame(tabControl, width=800, height=600, bg="#20bebe")
tab_seg = tk.Frame(tabControl, width=800, height=600, bg="#20bebe")

tab_start.pack(fill="both", expand=1)
tab_prep.pack(fill="both", expand=1)
tab_seg.pack(fill="both", expand=1)

tabControl.add(tab_start, text="Start")
tabControl.add(tab_prep, text="Preprocessing")
tabControl.add(tab_seg, text="Segmentacja")

param_prep = tk.LabelFrame(tab_prep, width=250, height=500, bg="#20bebe", text='Parametry')
# param_prep.grid(columnspan=2, rowspan=4, row=0, sticky=tk.E)
param_prep.pack(side="right", expand=False, padx=20, pady=10)

param_seg = tk.LabelFrame(tab_seg, width=250, height=500, bg="#20bebe", text='Parametry')
# param_seg.grid(columnspan=2, rowspan=4, row=0, sticky=tk.E)
# param_seg = tk.Frame(tab_seg)
param_seg.pack(side="right", expand=False, padx=20, pady=10)


## 1st TAB

def open_file():
    global filename
    global path
    browse_text.set("ładowanie...")
    filename = askopenfile(parent=tab_start, mode='rb', filetypes=[("Image file", "*.png")])
    if filename:
        path = filename.name
        print(path)
        img = ImageTk.PhotoImage(file=filename)

        img_label = tk.Label(tab_start, image=img, bg="white")
        img_label.image = img
        img_label.pack(anchor=tk.W, padx=50, pady=15)


        browse_text.set("Wybierz")
        n_prep_btn = tk.Button(tab_start, text=">> Preprocessing", command=lambda: next_tab(0), font=("Raleway", 13),
                               bg="white")
        n_prep_btn.pack(anchor=tk.SE, padx=15, pady=15)

        chng_btn = tk.Button(tab_start, text='Zmień', command=lambda: reset_prep(img_label, n_prep_btn), font=("Raleway", 13),
                             bg="white")
        chng_btn.pack(side="right", pady=15, padx=25, expand=False)

    return filename

    ## 2nd TAB - PREP

    # Sliders


down_tresh = tk.Scale(param_prep, from_=0, to=300, orient=tk.HORIZONTAL, command=print_val, label='down_tresh:',
                      sliderlength=20)
down_tresh.grid(row=0, column=1, pady=5)
down_tresh.set(0)

up_tresh = tk.Scale(param_prep, from_=0, to=300, orient=tk.HORIZONTAL, command=print_val, label='up_tresh:',
                    sliderlength=20)
up_tresh.grid(row=1, column=1, pady=5)
up_tresh.set(220)

left_tresh = tk.Scale(param_prep, from_=0, to=300, orient=tk.HORIZONTAL, command=print_val, label='left_tresh:',
                      sliderlength=20)
left_tresh.grid(row=2, column=1, pady=5)
left_tresh.set(10)

right_tresh = tk.Scale(param_prep, from_=0, to=300, orient=tk.HORIZONTAL, command=print_val, label='right_tresh:',
                       sliderlength=20)
right_tresh.grid(row=3, column=1, pady=5)
right_tresh.set(215)

gamma = tk.Scale(param_prep, from_=0, to=10, orient=tk.HORIZONTAL, command=print_val, resolution=0.1, label='gamma:',
                 sliderlength=20)
gamma.grid(row=4, column=1, pady=5)
gamma.set(1.2)

prep_btn = tk.Button(param_prep, text='Wykonaj',
                     command=lambda: prep_img(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma),
                     font=("Raleway", 12),
                     bg="white", fg="black", height=1, width=15)

prep_btn.grid(row=6, column=1, pady=15)

## 3rd TAB - SEG
## segmentation (img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min)

#     # Sliders
thresh = tk.Scale(param_seg, from_=0, to=300, orient=tk.HORIZONTAL, command=print_val, label='tresh:', sliderlength=20)
thresh.grid(row=0, column=1, pady=5)
thresh.set(100)

fg_tresh_max = tk.Scale(param_seg, from_=0, to=100, orient=tk.HORIZONTAL, command=print_val, label='fg_tresh_max:',
                        sliderlength=20)
fg_tresh_max.grid(row=1, column=1, pady=5)
fg_tresh_max.set(13)

fg_tresh_min = tk.Scale(param_seg, from_=0, to=100, orient=tk.HORIZONTAL, command=print_val, label='fg_tresh_min:',
                        sliderlength=20)
fg_tresh_min.grid(row=2, column=1, pady=5)
fg_tresh_min.set(11)

bg_tresh_max = tk.Scale(param_seg, from_=0, to=100, orient=tk.HORIZONTAL, command=print_val, label='bg_tresh_max:',
                        sliderlength=20)
bg_tresh_max.grid(row=3, column=1, pady=5)
bg_tresh_max.set(31)

bg_tresh_min = tk.Scale(param_seg, from_=0, to=100, orient=tk.HORIZONTAL, command=print_val, label='bg_tresh_min:',
                        sliderlength=20)
bg_tresh_min.grid(row=4, column=1, pady=5)
bg_tresh_min.set(11)
#
seg_btn = tk.Button(param_seg, text='Wykonaj',
                    command=lambda: seg_img(img_gamma, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min),
                    font=("Raleway", 12),
                    bg="white", fg="black", height=1, width=15)

seg_btn.grid(row=6, column=1, pady=15)

instructions = tk.Label(tab_start, text="Załaduj obraz do analizy:", font=("Raleway", 13), bg="#20bebe")
instructions.pack(anchor=tk.NE, pady=10, padx=10)

browse_text = tk.StringVar()
browse_btn = tk.Button(tab_start, textvariable=browse_text, command=lambda: open_file(), font=("Raleway", 12),
                       bg="white", fg="black", height=1, width=15)
browse_text.set("Wybierz")
browse_btn.pack(anchor=tk.NE, pady=10, padx=25)

root.mainloop()

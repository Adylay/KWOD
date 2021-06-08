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
from function import stenosis


def next_tab(ntab):
    tabControl.select(ntab + 1)


def print_val(var):
    print(var)


def reset_prep(label, button):
    label.destroy()
    button.pack_forget()


def reset_label(label):
    for widget in label.winfo_children():
        widget.destroy()


def getcoord(eventorigin):
    global x0, y0
    x0 = eventorigin.x
    y0 = eventorigin.y
    print(x0, y0)


def select_area():
    if img_label_alg.winfo_exists():
        img_label_alg.bind("<Button-1>", getcoord)
        area = (x0 - 24, y0 - 24, x0 + 25, y0 + 25)  # left, top, right, bottom
        img_in = Image.open(path)
        cropped_img = img_in.crop(area)
        new_image = cropped_img.resize((250, 250))
        new_image.save('image_crop.jpg')
        crop_img = ImageTk.PhotoImage(new_image)

        # width, height = img_in.size
        # print(width, height)

        top_c = tk.Toplevel()
        top_c.title('Przewężenie')
        top_c.iconbitmap('icon1.ico')

        img_label_c = tk.Label(top_c, image=crop_img, bg="white")
        img_label_c.image = crop_img
        img_label_c.grid(rowspan=3, column=0, row=1)

        (maxim, minim, zwezenie, label_dilation) = stenosis('image_crop.jpg')
        img2pil = Image.fromarray(label_dilation, "L")
        img_sgm1 = ImageTk.PhotoImage(img2pil)
        img_l1 = tk.Label(top_c, image=img_sgm1, bg="white")
        img_l1.image = img_sgm1
        img_l1.grid(rowspan=3, column=1, row=1)

        lbl_rez = tk.Label(top_c, text='Wyniki: ')
        lbl_rez.grid(column=2, row=1, sticky=tk.S)
        l1 = tk.Label(top_c,
                      text='maximum = {0} \nminimum = {1} \nprzewężenie = {2} \n '.format(
                          maxim, minim, zwezenie))
        l1.grid(column=2, row=2, sticky=tk.N)


def prep_img(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma):
    global img_gamma
    global top
    global img_gm
    global down_tresh_v, up_tresh_v, left_tresh_v, right_tresh_v, gamma_v
    down_tresh = down_tresh.get()
    up_tresh = up_tresh.get()
    left_tresh = left_tresh.get()
    right_tresh = right_tresh.get()
    gamma = gamma.get()
    down_tresh_v = down_tresh
    up_tresh_v = up_tresh
    left_tresh_v = left_tresh
    right_tresh_v = right_tresh
    gamma_v = gamma

    img_gamma = preprocesing(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma)

    img_pil = Image.fromarray(img_gamma, "L")

    img_gm = ImageTk.PhotoImage(img_pil)
    global img_label2
    img_label2 = tk.Label(param_obr, image=img_gm, bg="white")
    img_label2.image = img_gm
    img_label2.pack(side=tk.LEFT, padx=50)
    tab_prep.update_idletasks()

    global n_seg_btn
    n_seg_btn = tk.Button(param_prep, text=">> Segmentacja", command=lambda: next_tab(1), font=("Raleway", 13),
                          bg="white")
    n_seg_btn.grid(row=8, column=1, pady=15)

    print(path, down_tresh, up_tresh, left_tresh, right_tresh, gamma)

    rst_btn = tk.Button(param_prep, text="Reset", command=lambda: reset_label(param_obr),
                        font=("Raleway", 13),
                        bg="white")
    rst_btn.grid(row=7, column=1, pady=15)

    top = tk.Toplevel()
    top.title('Preprocessing Results')
    top.iconbitmap('icon1.ico')
    lbl = tk.Label(top, text='Obraz wejściowy', font=("Raleway", 10), bg='white')
    lbl.grid(column=0, row=0, sticky=tk.N)

    lbl1 = tk.Label(top, text='Po preprocessingu', font=("Raleway", 10), bg='white')
    lbl1.grid(column=1, row=0, sticky=tk.N)

    img_label_w = tk.Label(top, image=img, bg="white")
    img_label_w.image = img
    img_label_w.grid(rowspan=3, column=0, row=1)
    img_label_p = tk.Label(top, image=img_gm, bg="white")
    img_label_p.image = img_gm
    img_label_p.grid(rowspan=3, column=1, row=1)

    lbl_prm = tk.Label(top, text='Parametry: ')
    lbl_prm.grid(column=1, row=4, sticky=tk.W)
    l1 = tk.Label(top,
                  text='down_tresh = {0} \n up_tresh = {1} \n left_tresh = {2} \n right_tresh = {3} \n gamma = {4}'.format(
                      down_tresh, up_tresh, left_tresh, right_tresh, gamma))
    l1.grid(column=1, row=5, sticky=tk.W)


def seg_img(img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min):
    global img_label3
    thresh = thresh.get()
    fg_tresh_max = fg_tresh_max.get()
    fg_tresh_min = fg_tresh_min.get()
    bg_tresh_max = bg_tresh_max.get()
    bg_tresh_min = bg_tresh_min.get()

    img_seg = segmentation(img_gray_filtr, thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min)
    img_seg2 = img_seg * 250
    img_pil = Image.fromarray(img_seg2, "L")
    img_sgm = ImageTk.PhotoImage(img_pil)
    img_label3 = tk.Label(seg_obr, image=img_sgm, bg="white")
    img_label3.image = img_sgm
    img_label3.pack(side=tk.LEFT, padx=50)

    print(thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min)
    rst_btn2 = tk.Button(param_seg, text="Reset", command=lambda: reset_label(seg_obr), font=("Raleway", 13),
                         bg="white")
    rst_btn2.grid(row=7, column=1, pady=15)

    top = tk.Toplevel()
    top.title('Segmentation Results')
    top.iconbitmap('icon1.ico')
    lbl = tk.Label(top, text='Obraz wejściowy', font=("Raleway", 10), bg='white')
    lbl.grid(column=0, row=0, sticky=tk.N)

    lbl1 = tk.Label(top, text='Po preprocessingu', font=("Raleway", 10), bg='white')
    lbl1.grid(column=1, row=0, sticky=tk.N)

    lbl1 = tk.Label(top, text='Po segmentacji', font=("Raleway", 10), bg='white')
    lbl1.grid(column=2, row=0, sticky=tk.N)

    img_label_w = tk.Label(top, image=img, bg="white")
    img_label_w.image = img
    img_label_w.grid(rowspan=3, column=0, row=1)
    img_label_p = tk.Label(top, image=img_gm, bg="white")
    img_label_p.image = img_gm
    img_label_p.grid(rowspan=3, column=1, row=1)
    img_label_s = tk.Label(top, image=img_sgm, bg="white")
    img_label_s.image = img_sgm
    img_label_s.grid(rowspan=3, column=2, row=1)

    lbl_prm = tk.Label(top, text='Parametry: ')
    lbl_prm.grid(column=1, row=4, sticky=tk.W)
    l1 = tk.Label(top,
                  text='down_tresh = {0} \n up_tresh = {1} \n left_tresh = {2} \n right_tresh = {3} \n gamma = {4}'.format(
                      down_tresh_v, up_tresh_v, left_tresh_v, right_tresh_v, gamma_v))
    l1.grid(column=1, row=5, sticky=tk.W)

    lbl_sg = tk.Label(top, text='Parametry: ')
    lbl_sg.grid(column=2, row=4, sticky=tk.W)
    l2 = tk.Label(top,
                  text='tresh = {0} \n fg_tresh_max = {1} \n fg_tresh_min = {2} \n bg_tresh_max = {3} \n bg_tresh_min = {4}'.format(
                      thresh, fg_tresh_max, fg_tresh_min, bg_tresh_max, bg_tresh_min))
    l2.grid(column=2, row=5, sticky=tk.W)


def view_stenosis():
    top_c = tk.Toplevel()
    top_c.title('Przykład przewężenia')
    top_c.iconbitmap('icon1.ico')

    img_label_c = tk.Label(top_c, image=img_c, bg="white")
    img_label_c.image = img_c
    img_label_c.grid(rowspan=3, column=0, row=1)

    (maxim, minim, zwezenie, label_dilation) = stenosis(filename_c)

    img_pil = Image.fromarray(label_dilation, "L")
    img_sgm = ImageTk.PhotoImage(img_pil)
    img_l = tk.Label(top_c, image=img_sgm, bg="white")
    img_l.image = img_sgm
    img_l.grid(rowspan=3, column=1, row=1)

    lbl_rez = tk.Label(top_c, text='Wyniki: ')
    lbl_rez.grid(column=2, row=1, sticky=tk.S)
    l1 = tk.Label(top_c,
                  text='maximum = {0} \nminimum = {1} \nprzewężenie = {2} \n '.format(
                      maxim, minim, zwezenie))
    l1.grid(column=2, row=2, sticky=tk.N)


def open_crop_img():
    global img_c
    global path_c
    global filename_c
    filename_c = askopenfile(parent=tab_crop, mode='rb', filetypes=[("Image file", ("*.png", "*.jpg"))])
    if filename_c:
        path_c = filename_c.name
        print(path_c)

        img_c = ImageTk.PhotoImage(file=filename_c)

        img_label = tk.Label(crop_frame, image=img_c, bg="white")
        img_label.image = img_c
        img_label.grid(column=0, row=1, columnspan=2)

        btn = tk.Button(crop_frame, text='Oblicz', command=lambda: view_stenosis(),
                        font=("Raleway", 13), bg="white")
        btn.grid(column=1, row=3)


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
tab_crop = tk.Frame(tabControl, width=800, height=600, bg="#20bebe")

tab_start.pack(fill="both", expand=1)
tab_prep.pack(fill="both", expand=1)
tab_seg.pack(fill="both", expand=1)
tab_crop.pack(fill="both", expand=1)

tabControl.add(tab_start, text="Start")
tabControl.add(tab_prep, text="Preprocessing")
tabControl.add(tab_seg, text="Segmentacja")
tabControl.add(tab_crop, text="Przewężenia")

param_prep = tk.LabelFrame(tab_prep, width=250, height=500, bg="#20bebe", text='Parametry')
param_prep.pack(side="right", expand=False, padx=20, pady=10)

param_obr = tk.LabelFrame(tab_prep, text="Results", width=550, height=500, bg="#20bebe")
param_obr.pack(side="left", expand=True, padx=20, pady=10)

param_seg = tk.LabelFrame(tab_seg, width=250, height=500, bg="#20bebe", text='Parametry')
param_seg.pack(side="right", expand=False, padx=20, pady=10)

seg_obr = tk.LabelFrame(tab_seg, text="Results", width=550, height=500, bg="#20bebe")
seg_obr.pack(side="left", expand=False, padx=20, pady=10)

l = tk.Label(tab_crop, text='Wybierz przewężenie', font=("Raleway", 10), bg='white')
l.grid(column=0, row=0, sticky=tk.N)

crop_frame = tk.LabelFrame(tab_crop, width=350, height=500, bg="#20bebe", text='Wczytaj Przykład')
crop_frame.grid(sticky=tk.E, columnspan=3, rowspan=3, padx=20, pady=10, column=5, row=0)


## 1st TAB

def open_file():
    global filename
    global path
    global img
    global img_label_alg
    browse_text.set("ładowanie...")
    filename = askopenfile(parent=tab_start, mode='rb', filetypes=[("Image file", ("*.png", "*.jpg"))])
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

        chng_btn = tk.Button(tab_start, text='Zmień', command=lambda: reset_prep(img_label, n_prep_btn),
                             font=("Raleway", 13),
                             bg="white")
        chng_btn.pack(side="right", pady=15, padx=25, expand=False)

        img_label_alg = tk.Label(tab_crop, image=img, bg="white")
        img_label_alg.image = img
        img_label_alg.grid(columnspan=3, rowspan=3, column=0, row=1, padx=50, sticky=tk.N)

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

crop_btn = tk.Button(tab_crop, text='Wykonaj', command=lambda: select_area(), font=("Raleway", 12),
                     bg="white", fg="black", height=1, width=15)
crop_btn.grid(column=2, row=0, sticky=tk.NW)

crop_btn1 = tk.Button(tab_crop, text='Start', command=lambda: select_area(), font=("Raleway", 12),
                      bg="white", fg="black", height=1, width=15)
crop_btn1.grid(column=1, row=0, sticky=tk.N)

crop_btn2 = tk.Button(crop_frame, text='Wybierz wycinek', command=lambda: open_crop_img(), font=("Raleway", 12),
                      bg="white", fg="black", height=1, width=15)
crop_btn2.grid(column=1, row=0, sticky=tk.N)

root.mainloop()

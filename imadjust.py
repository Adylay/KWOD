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
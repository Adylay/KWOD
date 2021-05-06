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
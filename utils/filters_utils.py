from numpy import array,eye,zeros_like,multiply,dot,transpose
from skimage.color import rgb2gray
from numpy import full
from skimage import img_as_uint
def scalar_transform(thresh_val,image):

    thresh_val = thresh_val/255
    #print(img[0])
    eye_arr = eye(600,800, dtype=(float,3))
    ident = eye(800,800)
    thresh_arr = full((600,800),thresh_val)
    zer = zeros_like(thresh_arr)
    for i in range(200):
        zer[:,i] = -0.08
    #ident = eye(600, 800)
    #thresh_arr = full((600, 800), thresh_val)
    scalar = 0.3
    inc = 0
    i = 0
    while(i<200):
        thresh_arr[:,i] = thresh_arr[:,i] * (0.6+inc)
        i= i +1
        inc = inc + 0.002


    i = 600
    inc = 0
    while (i < 800):
        thresh_arr[:, i] = thresh_arr[:, i] * (1-inc)
        i = i + 1
        inc = inc + 0.002

    #horizontal
    i = 0
    inc = 0
    while (i < 200):
        thresh_arr[i, :] = thresh_arr[i, :] * (0.6+inc)
        i = i + 1
        inc = inc + 0.002
    i = 400
    inc = 0
    while (i < 600):
        thresh_arr[i, :] = thresh_arr[i, :] * (1-inc)
        inc = inc + 0.002
        i = i + 1




    print("shape:", thresh_arr.shape)
    return thresh_arr
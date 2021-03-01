from skimage.draw import set_color
from skimage.io import imsave
from skimage.draw import circle,circle_perimeter,rectangle_perimeter
import random
from numpy import array
def color_out_image(regions,image,multi,min=0,scale=2.5):

    for reg in regions:
        temp_set = {(1,0)}
        y_ls = []
        x_ls = []

        for pt in reg.coords:
            y_ls.append(pt[0])
            x_ls.append(pt[1])
            #z = pt[2]
            #temp_set.add((x,y))
        if multi:
            r = random.randint(0, 200)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        else:
            #r,g,b = 183,255,15
            r,g,b = 23,162,25
        scale = float(scale)
        if(scale*scale*len(reg.coords)>(float(min))):
            set_color(image, (array(y_ls),array(x_ls)), color =(r,g,b))
    return image




def color_out_image_large_area(region,image,color=(255, 1, 1)):
        #ut = image
        for pt in region.coords:
            x=pt[1]
            y=pt[0]
            #z=pt[2]
            set_color(image, (y, x), color=color)
        return image

def color_out_largest(region_ls, image):
    for region in region_ls[:3]:
        image = color_out_image_large_area(region, image)
    #for region in region_ls[2:]:
    #    image = color_out_image_large_area(region, image,color=(250,250,17))
    return image


def color_out_set(coord_set, image):
    #out_image = image
    #print("co[0]", coord_set[0])
    set_color(image, (coord_set[1],coord_set[0]), color=(0, 77, 253))
    return image


def color_circle(c,r,image):
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r)
    #set_color(image, (y_ls,x_ls), color=(0, 77, 253))
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-1)
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-2)
    set_color(image, (y_ls, x_ls), color=(255, 255, 255))


def color_holes(hole_ls, image):
    #print(len(hole_ls))
    for hole in hole_ls:
        color_circle(hole[4],hole[5],image)
    return image

def color_holes2(hole_ls, image):
    for hole in hole_ls:
        color_circle(hole[0],hole[1],image)
    return image


def add_boarder(image,boarder):
    y, x, z = image.shape
    for i in range(0, 5):
        coords = rectangle_perimeter(start=(boarder//2 + i, boarder//2 + i), end=(y - boarder//2 + i, x - boarder//2 + i))
        set_color(image, coords, (255, 0, 0))

    return image


def save_out_image(image,out_path):
    save_name = '.' + out_path
    imsave(save_name,image)
    print("saved image at",save_name)
    # io.imsave("." + self.image_out_path + "/" + self.name[:-4] + "_out.png", self.out_image)

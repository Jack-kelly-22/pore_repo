from skimage.measure import label,regionprops
from utils import image_utils, area_utils
def create_subImage(img,constants,name='subImage',
                    x0=0,x1=0,y0=0,y1=0,
                    num_circles=10,thresh=120):
    constants["use_alt"] = False
    constants["fiber_type"] = 'dark'
    constants['ignore_size']= 1
    constants['scale_factor'] = float(constants["scale"])
    constants['num_circles']: num_circles
    constants['thresh'] = thresh
    img_seg = area_utils.get_thresh_image(img,constants)
    porosity = area_utils.get_porosity(img_seg)
    label_image = label(img_seg)
    regions = regionprops(label_image)
    largest_areas, largest_regions, largest_holes = area_utils.get_largest_areas_simple(regions, constants)
    out_img = image_utils.color_out_image(regions,img,True)
    # out_img = image_utils.color_out_largest(largest_regions, image)
    out_img = image_utils.color_holes(largest_areas[:num_circles],out_img)
    print('len',len(out_img))
    subImage = {
        "name": name,
        "out_img": out_img,
        #"in_img": img,
        #"largest_areas": largest_areas,
        #"largest_regions": largest_regions,
        "largest_holes": largest_holes,
        "thresh": float(constants["scale"]),
        "scale": constants["scale_factor"],
        "constants": constants,
        'num_circles': num_circles,
        "x0":x0,"x1":x1,"y0":y0,"y1":y1
    }
    return subImage





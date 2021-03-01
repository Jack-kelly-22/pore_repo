from dash_app.components import dash_reusable_components as drc
from utils import image_utils, area_utils
from skimage.measure import label, regionprops
from cv2 import resize, INTER_CUBIC
class LiveImage:
    def __init__(self,img_data,constants):
        self.scale_factor = constants["scale"]
        self.name = 'temp'
        img_data = (drc.b64_to_numpy(img_data,False))
        #img =
        img = resize(img_data, dsize=(800, 600), interpolation=INTER_CUBIC)
        img_seg = area_utils.get_thresh_image(img,constants)
        label_image = label(img_seg,connectivity=1)
        self.regions = regionprops(label_image)
        self.porosity = area_utils.get_porosity(img_seg)
        self.out_image = image_utils.color_out_image(self.regions, img, constants['multi'])
        self.largest_areas, self.largest_regions,self.largest_circles = area_utils.get_largest_areas(self.regions, self)
        self.out_image = image_utils.color_out_largest(self.largest_regions, self.out_image)
        self.out_image = image_utils.color_holes(self.largest_areas,self.out_image)

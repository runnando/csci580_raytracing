from PIL import Image
import numpy as np
import time
from tqdm import tqdm
from .utils import colour_functions as cf
from .camera import Camera
from .utils.constants import *
from .utils.vector3 import vec3, rgb
from .ray import Ray, get_raycolor
from . import lights
from .backgrounds.skybox import SkyBox
from .backgrounds.panorama import Panorama


class Stage:
    def __init__(self, ambient_color=rgb(0.01, 0.01, 0.01), n=vec3(1.0, 1.0, 1.0)):
        """

        Args:
            ambient_color:
            n: default index of reflection is that of the air for all three colors
        """
        self.ambient_color = ambient_color
        self.n = n
        self.scene_primitives = []
        self.collider_list = []
        self.shadowed_collider_list = []
        self.Light_list = []

    def add_camera(self, look_from, look_at, **kwargs):
        self.camera = Camera(look_from, look_at, **kwargs)

    def add_dirlight(self, Ldir, color):
        self.Light_list.append(lights.DirectionalLight(Ldir.normalize(), color))

    def add_primitive(self, primitive):
        if primitive.shadow:
            self.shadowed_collider_list += primitive.collider_list
        self.scene_primitives.append(primitive)
        self.collider_list += primitive.collider_list

    def add_background(self, img, light_intensity=0.0, blur=0.0, spherical=False):
        primitive = Panorama(img, light_intensity=light_intensity, blur=blur) if spherical else SkyBox(img, light_intensity=light_intensity, blur=blur)
        self.scene_primitives.append(primitive)
        self.collider_list += primitive.collider_list

    def render(self, samples_per_pixel):
        print("Rendering Start...")
        t0 = time.time()
        color_RGBlinear = rgb(0.0, 0.0, 0.0)
        for i in tqdm(range(samples_per_pixel)):
            color_RGBlinear += get_raycolor(self.camera.get_ray(self.n), stage=self)

        # subsample antialiasing
        color_RGBlinear = color_RGBlinear / samples_per_pixel
        # gamma correction
        color = cf.sRGB_linear_to_sRGB(color_RGBlinear.to_array())
        print("Rendering End:", time.time() - t0)

        img_RGB = []
        for c in color:
            # average ray colors that fall in the same pixel. (antialiasing) 
            img_RGB += [Image.fromarray((255 * np.clip(c, 0, 1).reshape((self.camera.screen_height, self.camera.screen_width))).astype(np.uint8), "L")]

        return Image.merge("RGB", img_RGB)

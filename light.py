from .utils.constants import SKYBOX_DISTANCE
from abc import abstractmethod


class Light:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    @abstractmethod   
    def get_L(self):
        pass

    @abstractmethod
    def get_distance(self, M):
        pass

    @abstractmethod   
    def get_irradiance(self, dist_light, NdotL):
        pass


class DirectionalLight(Light):
    def __init__(self, Ldir, color):
        self.Ldir = Ldir
        self.color = color

    def get_L(self):
        return self.Ldir

    def get_distance(self, M):
        return SKYBOX_DISTANCE

    def get_irradiance(self, dist_light, NdotL):
        return self.color * NdotL

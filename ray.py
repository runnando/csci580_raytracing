from .utils.constants import *
from .utils.vector3 import vec3, extract, rgb
import numpy as np
from functools import reduce as reduce


class Ray:
    """Info of the ray and the media it's travelling"""

    def __init__(self, origin, dir, depth, n, reflection_depth, refraction_depth, diffuse_reflection_depth):
        """
        light ray
        Args:
            origin: ray origin
            dir: ray direction
            depth: number of the reflections + refractions
            n: index of refraction of the media in which the ray passes through
            reflection_depth: number of the reflections
            diffuse_reflection_depth: number of diffuse reflections
            refraction_depth: number of the refractions
        """
        self.origin = origin
        self.dir = dir
        self.n = n
        self.depth = depth
        self.reflection_depth = reflection_depth
        self.refraction_depth = refraction_depth
        self.diffuse_reflection_depth = diffuse_reflection_depth

    def extract(self, hit_mask):
        return Ray(self.origin.extract(hit_mask), self.dir.extract(hit_mask), self.depth, self.n.extract(hit_mask),
                   self.reflection_depth, self.refraction_depth, self.diffuse_reflection_depth)


class Hit:
    def __init__(self, distance, orientation, material, collider, surface):
        """
        interaction between light ray and surfaces
        Args:
            distance:
            orientation:
            material:
            collider:
            surface:
        """
        self.distance = distance
        self.orientation = orientation
        self.material = material
        self.collider = collider
        self.surface = surface
        self.u = None
        self.v = None
        self.N = None
        self.point = None

    def get_uv(self):
        if self.u is None:  # this is for prevent multiple computations of u,v
            self.u, self.v = self.collider.assigned_primitive.get_uv(self)
        return self.u, self.v

    def get_normal(self):
        if self.N is None:  # this is for prevent multiple computations of normal
            self.N = self.collider.get_N(self)
        return self.N


def get_raycolor(ray, stage):
    """
    light ray color is determined by the nearest hit object
    Args:
        ray: w*h num of rays (pixels)
        stage:

    Returns:

    """

    inters = [s.intersect(ray.origin, ray.dir) for s in stage.collider_list]
    # distances, hit_orientation: [num of colliders, num of rays (pixels)]
    distances, hit_orientation = zip(*inters)

    # get the shortest distance collision
    # nearest: [num of rays (pixels),]
    nearest = reduce(np.minimum, distances)
    color = rgb(0., 0., 0.)

    for (coll, dis, orient) in zip(stage.collider_list, distances, hit_orientation):
        # hit_mask: [num of rays (pixels),], boolean array. True indicates that ray (pixel) is hit
        hit_mask = (nearest != FARAWAY) & (dis == nearest)

        if np.any(hit_mask):
            material = coll.assigned_primitive.material
            hit_info = Hit(extract(hit_mask, dis), extract(hit_mask, orient), material, coll, coll.assigned_primitive)
            cc = material.get_color(stage, ray.extract(hit_mask), hit_info)
            color += cc.place(hit_mask)

    return color


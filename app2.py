from sightpy import *


def main():
    # setup stage
    mystage = Stage(ambient_color=rgb(0.05, 0.05, 0.05))
    mystage.add_camera(look_from=vec3(2.5 * np.sin(np.pi / 2 * 0.3), 0.25, 2.5 * np.cos(np.pi / 2 * 0.3) - 1.5),
                       look_at=vec3(0., 0.25, -1.5),
                       screen_width=400,
                       screen_height=300)
    mystage.add_dirlight(Ldir=vec3(0.52, 0.45, -0.5), color=rgb(0.15, 0.15, 0.15))

    mystage.add_background("stormydays.png")

    floor = Glossy(diff_color=image("checkered_floor.png", repeat=80.), n=vec3(1.2 + 0.3j, 1.2 + 0.3j, 1.1 + 0.3j),
                   roughness=0.2, spec_coeff=0.3, diff_coeff=0.9)
    mystage.add_primitive(
        Plane(material=floor, center=vec3(0, -0.5, -3.0), width=120.0, height=120.0, u_axis=vec3(1.0, 0, 0),
              v_axis=vec3(0, 0, -1.0), max_ray_depth=3))

    # setup objects
    # n: index of refraction, a complex num
    n_blue = vec3(1.5 + 4e-8j, 1.5 + 4e-8j, 1.5 + 0.j)
    n_green = vec3(1.5 + 4e-8j, 1.5 + 0.j, 1.5 + 4e-8j)
    n_red = vec3(1.5 + 0.j, 1.5 + 5e-8j, 1.5 + 5e-8j)
    mystage.add_primitive(
        Sphere(material=Refractive(n=n_blue), center=vec3(-1.2, 0.0, -1.5), radius=.5, shadow=False, max_ray_depth=3))
    mystage.add_primitive(
        Sphere(material=Refractive(n=n_green), center=vec3(0., 0.0, -1.5), radius=.5, shadow=False, max_ray_depth=3))
    mystage.add_primitive(
        Sphere(material=Refractive(n=n_red), center=vec3(1.2, 0.0, -1.5), radius=.5, shadow=False, max_ray_depth=3))

    # rendering
    img = mystage.render(samples_per_pixel=8)
    img.save("app2.png")
    img.show()

    return


if __name__ == "__main__":
    main()

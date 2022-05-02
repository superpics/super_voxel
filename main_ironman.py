from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(0, (214/255, 186/255, 102/255))
scene.set_background_color((214/255, 186/255, 102/255))
scene.set_directional_light((1, 1, 1), 1, (0.5, 0.5, 0.5))


@ti.func
def process_box(src, x_size, y_size, z_size, color, mat, symmetric):
    for x, y, z in ti.ndrange((src[0], src[0] + x_size), (src[1], src[1] + y_size), (src[2], src[2] + z_size)):
        scene.set_voxel(ivec3(x, y, z), mat, color)
        if symmetric:
            scene.set_voxel(ivec3(-x, y, z), mat, color)

@ti.func
def process_header(x_source: int, y_source: int, z_source: int, x_size: int, y_size: int, z_size: int):
    for i in range(4):
        for x, y, z in ti.ndrange((x_source, x_source + x_size), (y_source, y_source + y_size), (z_source, z_source + z_size)):
            center = ivec3((x_size / 2 + x_source), (y_size / 2 + y_source + i), (z_size / 2 + z_source))
            if distance(center, ivec3(x, y + i, z)) < 4:
                scene.set_voxel(ivec3(x, y + i, z), 1, vec3(0.83, 0.72, 0.4) if 4 == z else vec3(0.9, 0.1, 0.1))

@ti.func
def make_dirt():
    y_offset = 6
    for x, y, z in ti.ndrange((-64, 64), (0, 30), (-64, 64)):
        if 10 < distance(ivec3(0, y, 0), ivec3(x, y, z)) < 35:
            if -4 <= ((x * x) / 200) + ((z * z) / 200) - ((y * y) / 10) <= -3:
                if ti.random() > 0.9:
                    scene.set_voxel(ivec3(x, y - y_offset, z), 1, vec3(1, 1, 1))

@ti.kernel
def initialize_voxels():
    h = 15
    # process_box(vec3(0, 0, 0), 1, 1, 1, vec3(1, 0, 0), 1, False)
    # process_box(vec3(0, 1, 0), 1, 1, 1, vec3(0, 1, 0), 1, False)

    # 脚
    process_box(vec3(-2, 0 + h, 0), 2, 3, 2, vec3(0.9, 0.1, 0.1), 1, True)
    process_box(vec3(-2, 0 + h, 2), 2, 1, 1, vec3(0.9, 0.1, 0.1), 1, True)
    process_box(vec3(-2, 3 + h, 0), 2, 2, 2, vec3(0.784, 0.65, 0.254), 1, True)
    process_box(vec3(-1, 2 + h, 0), 1, 1, 2, vec3(0.784, 0.65, 0.254), 1, True)
    # 火焰
    process_box(vec3(-2, 5, 0), 1, h - 5, 1, vec3(1, 1, 1), 2, True)
    process_box(vec3(-4, 0.4 * h + 5, 0), 1, h * 0.6, 1, vec3(1, 1, 1), 2, True)
    # 身体
    process_box(vec3(-3, 5 + h, 0), 4, 5, 2, vec3(0.9, 0.1, 0.1), 1, True)
    process_box(vec3(0, 5 + h, 2), 2, 5, 1, vec3(0.9, 0.1, 0.1), 1, True)
    process_box(vec3(-2, 6 + h, 2), 1, 3, 1, vec3(0.9, 0.1, 0.1), 1, True)
    # 反应炉
    process_box(vec3(0, 8 + h, 2), 1, 1, 1, vec3(1, 1, 1), 2, False)
    # 手
    process_box(vec3(-4, 5 + h, 0), 1, 1, 2, vec3(0.9, 0.1, 0.1), 1, True)
    # 头
    process_header(-4, 9 + h, 0-4, 8, 8, 10)
    process_box(vec3(-2, 18 + h, 3), 1, 1, 1, vec3(0.784, 0.65, 0.254), 1, True)
    process_box(vec3(-2, 11 + h, 3), 1, 1, 1, vec3(0.784, 0.65, 0.254), 1, True)
    # 红色额头
    process_box(vec3(-1, 18 + h, 4), 2, 1, 1, vec3(0.9, 0.1, 0.1), 1, True)
    # 下巴
    process_box(vec3(-1, 10 + h, 3), 2, 1, 2, vec3(0.83, 0.72, 0.4), 1, True)
    # 嘴巴
    process_box(vec3(-1, 11 + h, 3), 2, 1, 2, vec3(0.733, 0.596, 0.188), 1, True)
    # 眼睛
    process_box(vec3(-2, 15 + h, 4), 2, 1, 1, vec3(1, 1, 1), 2, True)

    make_dirt()


initialize_voxels()
scene.finish()

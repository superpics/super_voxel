from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=1)
scene.set_floor(-0.05, (214/255, 186/255, 102/255))
scene.set_background_color((214/255, 186/255, 102/255))
scene.set_directional_light((1, 1, 1), 1, (1, 1, 1))


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
def make_dirt(base, n):
    center = ti.Vector([0, 0])
    for i, j in ti.ndrange((-n, n), (-n, n)):
        i3 = ti.Vector([i, j])
        dis = ti.pow(ti.max(0, 1 - ti.math.distance(i3, center)/n) * 1.1, 3)
        height = (ti.random() * n * dis * 1)
        for k in ti.ndrange((-height*.6+base, height*1.2+base)):
            if 0 < k < 5 and dis*.1 > ti.random():
                scene.set_voxel(vec3(i, k, j), 2, vec3(0.952, 0.882, 0.674) if ti.random() > 0.1 else vec3(1, 1, 1))


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
    process_box(vec3(-2, 0.6 * h, 0), 1, h * 0.4, 1, vec3(1, 1, 1), 2, True)
    process_box(vec3(-4, 5, 0), 1, 5 + h - 5, 1, vec3(1, 1, 1), 2, True)
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
    # 额头红色
    process_box(vec3(-1, 18 + h, 4), 2, 1, 1, vec3(0.9, 0.1, 0.1), 1, True)
    # 下巴
    process_box(vec3(-1, 10 + h, 3), 2, 1, 2, vec3(0.83, 0.72, 0.4), 1, True)
    # 嘴巴
    process_box(vec3(-1, 11 + h, 3), 2, 1, 2, vec3(0.733, 0.596, 0.188), 1, True)
    # 眼睛
    process_box(vec3(-2, 15 + h, 4), 2, 1, 1, vec3(1, 1, 1), 2, True)

    make_dirt(0, 35)


initialize_voxels()
scene.finish()

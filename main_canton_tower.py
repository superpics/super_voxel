from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=1)
scene.set_floor(-100, vec3(0, 1, 1))
scene.set_background_color((214/255, 186/255, 102/255))
scene.set_directional_light((1, 1, 1), 1, (1, 1, 1))

@ti.kernel
def initialize_voxels():
    # 塔身
    y_offset = 7
    for x, y, z in ti.ndrange((-64, 64), (-64 + y_offset, 36 + y_offset), (-64, 64)):
        if ((x * x) / 3) + ((z * z) / 3) - ((y * y) / 150) <= 3:
            if ((x * x) / 3) + ((z * z) / 3) - ((y * y) / 150) == 3:
                scene.set_voxel(ivec3(x, y - y_offset, z), 2, vec3(1, 1, 1))
            else:
                scene.set_voxel(ivec3(x, y - y_offset, z), 1, vec3(1, 1, 1))

    # 天线
    for y in ti.ndrange((36, 64)):
        if y < 45:
            scene.set_voxel(ivec3(0, y, 0), 1, vec3(1, 1, 1))
        else:
            scene.set_voxel(ivec3(0, y, 0), 1, vec3(1, 104 / 255, 104 / 255) if y % 2 == 1 else vec3(1, 1, 1))

    # 天线灯
    scene.set_voxel(ivec3(0, 63, 0), 2, vec3(1, 104 / 255, 104 / 255))

    # 地板
    for x, z in ti.ndrange((-64, 64), (-64, 64)):
        scene.set_voxel(ivec3(x, -64, z), 1, vec3(0, 1, 1))


initialize_voxels()
scene.finish()

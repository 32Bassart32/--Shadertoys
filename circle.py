# reference ==> 

import taichi as ti

ti.init(arch = ti.cpu)

res_x = 512
res_y = 512
scatter = 1
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))

@ti.func
def smoothstep(v_min, v_max, v):
    assert(v_min < v_max)
    if v < v_min:
        v = v_min
    elif v > v_max:
        v = v_max
    t = (v-v_min) / float(v_max-v_min)

    return -2 * t**3 + 3 * t ** 2

@ti.func
def linearstep(v_min, v_max, v):
    assert(v_min < v_max)
    if v < v_min:
        v = v_min
    elif v > v_max:
        v = v_max
    t = (v-v_min) / float(v_max-v_min)

    return t

@ti.kernel
def render(t:ti.f32):
    center = ti.Vector([res_x//scatter//2, res_y//scatter//2])
    r1 = 100.0 / scatter

    for i,j in pixels:     
        color = ti.Vector([1.0, 1.0, 1.0]) # init your canvas to white
        pos = ti.Vector([i//scatter, j//scatter])
        r = (pos - center).norm() 

        # # discrete circle
        # if r <= r1:
        #     color = ti.Vector([0.0, 0.0, 0.0])

        # # smooth circle
        # color = ti.Vector([1.0, 1.0, 1.0]) * r/r1 

        # # smooth circle 2
        # color = ti.Vector([1.0, 1.0, 1.0]) * smoothstep(0.8, 1.0, r/r1)

        pixels[i, j] = color

gui = ti.GUI("Solid Circle", res=(res_x, res_y))

for i in range(100000):
    t = i * 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
import numpy as np
import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import pylinalg as la
from lupa.lua54 import LuaRuntime

import bindings

lua = LuaRuntime()

lua.globals()["game"] = bindings.game

canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
renderer.blend_mode = "weighted_plus"

bindings.game["renderer"] = renderer

with open("game/init.lua","r") as f:
    g = lua.execute(f.read())

g.init_scene()

camera = gfx.OrthographicCamera(512, 512)
camera.show_object(g.scene)

controller = gfx.PanZoomController(camera, register_events=renderer)


# initial camera state
camera_state = camera.get_state()

def animate():
    g.onFrame()
    renderer.render(g.scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
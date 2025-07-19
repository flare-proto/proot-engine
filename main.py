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

with open("game/init.lua","r") as f:
    g = lua.execute(f.read())

g.init_scene()

def animate():
    g.onFrame()
    renderer.render(g.scene, g.camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
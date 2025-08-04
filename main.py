import numpy as np
import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import pylinalg as la
import pickle
from lupa.lua54 import LuaRuntime # type: ignore
from wgpu.utils.imgui import ImguiRenderer
from imgui_bundle import imgui, hello_imgui, icons_fontawesome_6  # type: ignore

import bindings,sys

lua = LuaRuntime()

lua.globals()["game"] = bindings.game # type: ignore

canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
renderer.blend_mode = "weighted_plus"

bindings.game["renderer"] = renderer

with open("game/init.lua","r") as f:
    g = lua.execute(f.read())

g.init_scene() # type: ignore

gui_renderer = ImguiRenderer(renderer.device, canvas)

state = {"pause": False}

fa_loading_params = hello_imgui.FontLoadingParams()
fa_loading_params.use_full_glyph_range = True
fa = hello_imgui.load_font("fonts/0xProtoNerdFont-Regular.ttf", 14, fa_loading_params)
gui_renderer.backend.create_fonts_texture()



camera = gfx.OrthographicCamera(512, 512)
camera.show_object(g.scene)

#controller = gfx.PanZoomController(camera, register_events=renderer)
controller = gfx.OrbitController(camera, register_events=renderer)

# initial camera state

state = {
    "model": True,
    "skeleton": False,
    "selected_action": 2,
}

camera_state = camera.get_state()


def draw_imgui():
    imgui.new_frame()
    #imgui.set_next_window_size((250, 0), imgui.Cond_.always)
    
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_save, _ = imgui.menu_item("Save", "Cmd+S", False, True)
            if clicked_save:
                pass
            clicked_quit, _ = imgui.menu_item("Quit", "Cmd+Q", False, True)
            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        if imgui.begin_menu("Edit", True):
            clicked_quit, _ = imgui.menu_item("TEST", "", False, True)
            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        if imgui.begin_menu("Build", True):
            clicked_quit, _ = imgui.menu_item("Lua Mappings", "", False, True)
            if clicked_quit:
                bindings.build_mappings()

            imgui.end_menu()
        if imgui.begin_menu("Run", True):
            clicked_quit, _ = imgui.menu_item("TEST", "", False, True)
            if clicked_quit:
                sys.exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()
        
    imgui.set_next_window_pos(
        (0, 20), imgui.Cond_.always
    )
    is_expand, _ = imgui.begin(
        "Controls",
        None,
        2|4|32|64
    )
    if is_expand:
        if imgui.collapsing_header("Transform", imgui.TreeNodeFlags_.default_open): # pyright: ignore[reportCallIssue, reportArgumentType]
            valu = 88.0, 42.0, 69.0
            changed, values = imgui.input_float3(
                "Position",valu # pyright: ignore[reportArgumentType]
            )
            changed, values = imgui.input_float3(
                "Rotation",(0,0,0) # pyright: ignore[reportArgumentType]
            )
            changed, values = imgui.input_float3(
                "Scale",(0,0,0) # pyright: ignore[reportArgumentType]
            )
        if imgui.collapsing_header("Visibility", imgui.TreeNodeFlags_.default_open): # pyright: ignore[reportCallIssue, reportArgumentType]
            _, state["model"] = imgui.checkbox("show model", state["model"])

            _, state["skeleton"] = imgui.checkbox("show skeleton", state["skeleton"])

        if imgui.collapsing_header("Animations", imgui.TreeNodeFlags_.default_open):# pyright: ignore[reportCallIssue, reportArgumentType]
            selected, state["selected_action"] = imgui.combo( # pyright: ignore[reportArgumentType]
                "Animation",
                state["selected_action"],
                ["A","B","C"],
                3
            )

    imgui.end()


    imgui.end_frame()
    imgui.render()
    return imgui.get_draw_data()



gui_renderer.set_gui(draw_imgui)

def on_key_down(event):
    print(f"Key pressed: {event['key']}")

canvas.add_event_handler(on_key_down, "key_down")

def on_key_down(event):
    print(f"Key pressed: {event['key']}")

canvas.add_event_handler(on_key_down, "key_down")

def animate():
    g.onFrame()
    renderer.render(g.scene, camera)
    gui_renderer.render()
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
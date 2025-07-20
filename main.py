import numpy as np
import imageio.v3 as iio
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import pylinalg as la
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
fa = hello_imgui.load_font("fonts/fontawesome-webfont.ttf", 14, fa_loading_params)
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
    imgui.set_next_window_size((250, 0), imgui.Cond_.always)
    imgui.set_next_window_pos(
        (gui_renderer.backend.io.display_size.x - 250, 0), imgui.Cond_.always
    )
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
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
            clicked_quit, _ = imgui.menu_item("Mappings", "Build Mappings", False, True)
            if clicked_quit:
                bindings.build_mappings()

            imgui.end_menu()
        imgui.end_main_menu_bar()
    is_expand, _ = imgui.begin(
        "Controls",
        None,
        flags=imgui.WindowFlags_.no_move | imgui.WindowFlags_.no_resize,
    )
    if is_expand:
        if imgui.collapsing_header("Visibility", imgui.TreeNodeFlags_.default_open):
            _, state["model"] = imgui.checkbox("show model", state["model"])

            _, state["skeleton"] = imgui.checkbox("show skeleton", state["skeleton"])

        if imgui.collapsing_header("Animations", imgui.TreeNodeFlags_.default_open):
            selected, state["selected_action"] = imgui.combo(
                "Animation",
                state["selected_action"],
                ["A","B","C"],
                3
            )

    imgui.end()

    imgui.set_next_window_size(
        (gui_renderer.backend.io.display_size.x, 0), imgui.Cond_.always
    )
    imgui.set_next_window_pos(
        (0, gui_renderer.backend.io.display_size.y - 40), imgui.Cond_.always
    )
    imgui.begin(
        "player",
        True,
        flags=imgui.WindowFlags_.no_move
        | imgui.WindowFlags_.no_resize
        | imgui.WindowFlags_.no_collapse
        | imgui.WindowFlags_.no_title_bar,
    )


    imgui.push_font(fa)
    

    imgui.pop_font()
    imgui.same_line()
    avail_size = imgui.get_content_region_avail()
    imgui.set_next_item_width(avail_size.x)
    
    imgui.end()

    imgui.end_frame()
    imgui.render()
    return imgui.get_draw_data()



gui_renderer.set_gui(draw_imgui)

def animate():
    g.onFrame()
    renderer.render(g.scene, camera)
    gui_renderer.render()
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
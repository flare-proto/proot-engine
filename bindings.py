import functools
import inspect
import textwrap
from typing import get_type_hints,Any,Tuple,Callable
import pylinalg as la
import numpy as np

import pygfx,proot

type Callback = Callable[pygfx.Event,None]

lua_bindings = {}
custom_type_map = {}

def register_lua_type(py_type, lua_type_name: str):
    """Register a custom Python-to-Lua type mapping."""
    custom_type_map[py_type] = lua_type_name

def python_type_to_lua(py_type):
    """Map Python types to Lua types, including registered custom types."""
    print(py_type,type(py_type))
    if py_type in custom_type_map:
        return custom_type_map[py_type]

    mapping = {
        int: "number",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "table",
        dict: "table",
        type(None): "nil",
    }
    return mapping.get(py_type, "any")

register_lua_type(pygfx.Geometry,"Geometry")
register_lua_type(pygfx.Material,"Material")
register_lua_type(pygfx.Scene,"Scene")
register_lua_type(pygfx.Mesh,"Mesh")
register_lua_type(pygfx.PerspectiveCamera,"Camera")
register_lua_type(pygfx.Light,"Light")
register_lua_type(Tuple[float, float, float],"Vec3")
register_lua_type(np.ndarray,"ndarray")
register_lua_type(proot.Actor,"Actor")
register_lua_type(Callback,"function")

def bind(namespace,lua_func_name):
    def fx(func):
        nonlocal lua_func_name
        namespace[lua_func_name] = func
        func_name = (f"{namespace.get("_NS_PATH",None)}.{lua_func_name}").removeprefix(".")
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        param_docs = []
        lua_params = []

        for name, param in sig.parameters.items():
            param_type = type_hints.get(name, None)
            lua_type = python_type_to_lua(param_type)
            param_docs.append(f"--- @param {name} {lua_type}")
            lua_params.append(name)

        # Return type
        return_type = type_hints.get('return', None)
        return_doc = f"--- @return {python_type_to_lua(return_type)}" if return_type else ""
        
        if return_doc:
            param_docs.append(return_doc)

        lua_func = textwrap.dedent(f"""
{"\n".join(param_docs)}
function {func_name}({", ".join(lua_params)})
    --return py_call("{func.__name__}", {{ {", ".join(lua_params)} }})
end""")

        lua_bindings[func_name] = lua_func.strip()

        return func
    return fx

game:dict[str,Any] = {
    "_NS_PATH":"game"
}
scene:dict[str,Any] = {
    "_NS_PATH":"game.scene",
    
}

game["scene"] = scene

background:dict[str,Any] = {
    "_NS_PATH":"game.scene.background",
}
scene["background"] = background

geometry:dict[str,Any] = {
    "_NS_PATH":"game.scene.geometry",
}
scene["geometry"] = geometry

material:dict[str,Any] = {
    "_NS_PATH":"game.scene.material",
}
scene["material"] = material

light:dict[str,Any] = {
    "_NS_PATH":"game.scene.light",
}
scene["light"] = light

util:dict[str,Any] = {
    "_NS_PATH":"game.util",
}
game["util"] = util

@bind(game,"on")
def on(func:Callback,evt:str):
    rend:pygfx.renderers.WgpuRenderer = game["renderer"]
    rend.add_event_handler(func,evt)

@bind(scene,"mesh")
def makeMesh(geometry:pygfx.Geometry,material:pygfx.Material) -> pygfx.Mesh:
    return pygfx.Mesh(geometry,material)

@bind(scene,"scene")
def makeScene() -> pygfx.Scene:
    return pygfx.Scene()

@bind(scene,"camera")
def makeCamera(fov:int,aspect:int)->pygfx.PerspectiveCamera:
    return pygfx.PerspectiveCamera(fov,aspect)

@bind(scene,"OrthographicCamera")
def OrthographicCamera(w:int,h:int)->pygfx.OrthographicCamera:
    return pygfx.OrthographicCamera(w,h)

@bind(background,"color")
def setBackgroundColor(scn:pygfx.Scene,color: str):
    scn.add(pygfx.Background.from_color(color))
    
@bind(geometry,"box")
def box(w:int,h:int,d:int) -> pygfx.Geometry:
    return pygfx.box_geometry(w,h,d)

@bind(geometry,"axes")
def axes(size:int,thick:int) -> pygfx.WorldObject:
    return pygfx.AxesHelper(size,thick)

@bind(material,"proto")
def protoMaterial() -> pygfx.Material:
    return pygfx.MeshPhongMaterial()

@bind(light,"ambientLight")
def AmbientLight() -> pygfx.Light:
    return pygfx.AmbientLight()

@bind(light,"directionalLight")
def DirectionalLight() -> pygfx.Light:
    return pygfx.DirectionalLight()

@bind(util,"quat_from_euler")
def quat_from_euler(euler: Tuple[float,float,float])->np.ndarray:
    return la.quat_from_euler(euler)

@bind(util,"quat_mul")
def quat_mul(q1:np.ndarray,q2:np.ndarray)->np.ndarray:
    return la.quat_mul(q1,q2)

@bind(scene,"actor")
def makeActor(name:str="") -> proot.Actor:
    return proot.Actor(name=name)

print(lua_bindings)

with open("gen/engine.lua","w") as f:
    f.write("""-- Autogened typings
--#region Namespace
game = {
    util = {},
    scene = {
        background = {},
        geometry = {},
        material = {},
        light = {}
    }
}   
--#endregion Namespace
--#region bindings
""")
    for k,v in lua_bindings.items():
        f.write(v)
        f.write("\n\n")
    f.write('--#endregion bindings')
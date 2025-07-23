--TODO remap WorldObject.local to WorldObject.localTransform

---@class WorldObject
---@field local AffineTransform
---@field world AffineTransform
local WorldObject = {}

---@param func function
---@param on string
function WorldObject.add_event_handler(func,on)
    
end

---@param obj WorldObject 
---@return WorldObject
function WorldObject.add(obj)
    
end

---@class Scene
local Scene = {}

---@param obj WorldObject 
function Scene.add(obj)
    
end

---@class Mesh:WorldObject
local Mesh = {}

---@class Light:WorldObject
local Light = {}

---@class Camera:WorldObject
local Camera = {}

---@param obj WorldObject
function Camera.show_object(obj)
    
end

---@class ndarray
local ndarray = {}


---@class AffineTransform
---@field x number
---@field y number
---@field z number
---@field euler_x number
---@field euler_y number
---@field euler_z number
---@field rotation ndarray
local AffineTransform = {}

---@class Actor:WorldObject
---@field localTransform AffineTransform
local Actor = {}
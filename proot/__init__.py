import pygfx

class Actor(pygfx.WorldObject):
    def __init__(self, geometry: pygfx.Geometry | None = None, material: pygfx.Material | None = None, *, visible: bool = True, render_order: float = 0, render_mask: str | int = "auto", name: str = "") -> None:
        super().__init__(geometry, material, visible=visible, render_order=render_order, render_mask=render_mask, name=name)
        self.localTransform = self.local
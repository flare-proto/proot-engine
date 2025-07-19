local test = {}
function init_scene()
    local scene = game.scene.scene()
    game.scene.background.color(scene,"#111")
    local box = game.scene.mesh(
        game.scene.geometry.box(200,200,200),
        game.scene.material.proto()
    )
    scene.add(box)
end
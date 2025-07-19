local test = {}
function test.init_scene()
    local scene = game.scene.scene()
    local camera = game.scene.camera(70,16/9)
    game.scene.background.color(scene,"#111")
    local box = game.scene.mesh(
        game.scene.geometry.box(200,200,200),
        game.scene.material.proto()
    )
    box.world.x = 150
    scene.add(box)
    scene.add(game.scene.light.ambientLight())

    scene.add(camera.add(game.scene.light.directionalLight()))

    test.scene = scene
    test.camera = camera

    camera.show_object(scene)
end

return test
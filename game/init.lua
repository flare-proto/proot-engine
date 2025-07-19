local test = {}
function test.init_scene()
    local scene = game.scene.scene()
    local camera = game.scene.camera(70,16/9)
    scene.add(game.scene.geometry.axes(20,2))
    game.scene.background.color(scene,"#222")
    local box0 = game.scene.mesh(
        game.scene.geometry.box(100,100,100),
        game.scene.material.proto()
    )
    local box = game.scene.actor("box")
    scene.add(box.add(box0))
    box.world.x = 150

    local box2 = game.scene.mesh(
        game.scene.geometry.box(100,100,100),
        game.scene.material.proto()
    )
    box2.world.x = -150
    scene.add(box2)

    scene.add(game.scene.light.ambientLight())

    scene.add(camera.add(game.scene.light.directionalLight()))

    test.scene = scene
    test.camera = camera

    camera.show_object(scene)

    function test.onFrame()
        local rot = game.util.quat_from_euler({0.005, 0,0})
        box.localTransform.rotation = game.util.quat_mul(rot, box.localTransform.rotation)
    end
end

return test
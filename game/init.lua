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
    box.localTransform.x = 150

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
    game.util.save(scene)
    function test.onFrame()
        
        box.localTransform.euler_x =box.localTransform.euler_x + 0.1
    end
end

return test
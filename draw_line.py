from OpenGL.GL import *
from pyrr import Vector3

from edge import EdgeHandler, EdgeRenderer
from file import FileHandler
from window import WindowHandler

WIDTH, HEIGHT = 1920, 1080

window_handler = WindowHandler()
window = window_handler.create_window("Testing", WIDTH, HEIGHT, 1)
window.set_position(0, 0)
window.set_callbacks()
window.activate()

layer_one = [-0.75, -0.5, 0.0,
             -0.75, 0.0, 0.0,
             -0.75, 0.5, 0.0,
             -0.75, -0.5, -0.5,
             -0.75, 0.0, -0.5,
             -0.75, 0.5, -0.5,
             -0.75, -0.5, 0.5,
             -0.75, 0.0, 0.5,
             -0.75, 0.5, 0.5]
layer_two = [0.75, -0.5, 0.0,
             0.75, 0.0, 0.0,
             0.75, 0.5, 0.0,
             0.75, -0.5, -0.5,
             0.75, 0.0, -0.5,
             0.75, 0.5, -0.5,
             0.75, -0.5, 0.5,
             0.75, 0.0, 0.5,
             0.75, 0.5, 0.5]

sample_length = (Vector3([-0.5, -0.3, 0.0]) - Vector3([0.5, -0.3, 0.0])).length / 50.0
edge_handler = EdgeHandler(sample_length, True)
edge_handler.set_data(layer_one, layer_two)
edge_handler.sample_edges()

edge_renderer = EdgeRenderer(edge_handler)

FileHandler().read_statistics()
render_loop_index: int = 0
while window.is_active():
    window_handler.update()

    edge_handler.sample_edges()
    #edge_handler.sample_noise(0.5)

    edge_renderer.render_transparent(window)

    window.swap()
    render_loop_index += 1

FileHandler().write_statistics()
window_handler.destroy()

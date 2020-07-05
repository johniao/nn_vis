from typing import Dict

from OpenGL.GL import *

from models.grid import Grid
from opengl_helper.render_utility import VertexDataHandler, RenderSet, render_setting_0, render_setting_1
from opengl_helper.shader import RenderShaderHandler, RenderShader
from processing.node_processing import NodeProcessor
from utility.camera import Camera
from utility.performance import track_time
from utility.window import Window


class NodeRenderer:
    def __init__(self, node_processor: NodeProcessor, grid: Grid):
        self.node_processor = node_processor
        self.grid = grid

        shader_handler: RenderShaderHandler = RenderShaderHandler()
        node_point_shader: RenderShader = shader_handler.create("node_point", "node/sample.vert",
                                                                "basic/discard_screen_color.frag")
        node_sphere_shader: RenderShader = shader_handler.create("node_sphere", "node/sample_impostor.vert",
                                                                 "node/point_to_sphere_impostor_phong.frag",
                                                                 "node/point_to_sphere_impostor.geom")
        node_transparent_shader: RenderShader = shader_handler.create("node_transparent_sphere",
                                                                      "node/sample_impostor.vert",
                                                                      "node/point_to_sphere_impostor_transparent.frag",
                                                                      "node/point_to_sphere_impostor.geom")

        self.data_handler: VertexDataHandler = VertexDataHandler([(self.node_processor.node_buffer, 0)])

        self.point_render: RenderSet = RenderSet(node_point_shader, self.data_handler)
        self.sphere_render: RenderSet = RenderSet(node_sphere_shader, self.data_handler)
        self.sphere_render.set_uniform_label(
            [("Size", "object_radius"), ("Importance Threshold", "importance_threshold")])

        self.transparent_render: RenderSet = RenderSet(node_transparent_shader, self.data_handler)
        self.transparent_render.set_uniform_label(
            [("Size", "object_radius"), ("Base Opacity", "base_opacity"),
             ("Importance Opacity", "importance_opacity"), ("Depth Opacity", "depth_opacity"),
             ("Density Exponent", "opacity_exponent"), ("Importance Threshold", "importance_threshold")])

    @track_time
    def render_point(self, cam: Camera, options: Dict[str, float] = None, show_class: int = 0):
        node_count: int = len(self.node_processor.nodes)

        self.point_render.set_uniform_data([("projection", cam.projection, "mat4"),
                                            ("view", cam.view, "mat4"),
                                            ("screen_width", 1920.0, "float"),
                                            ("screen_height", 1080.0, "float")])
        self.point_render.set_uniform_labeled_data(options)

        self.point_render.set()

        render_setting_0(False)
        glPointSize(10.0)
        glDrawArrays(GL_POINTS, 0, node_count)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)

    @track_time
    def render_sphere(self, cam: Camera, sphere_radius: float = 0.03, options: Dict[str, float] = None,
                      show_class: int = 0):
        node_count: int = len(self.node_processor.nodes)

        self.sphere_render.set_uniform_data([("projection", cam.projection, "mat4"),
                                             ("view", cam.view, "mat4"),
                                             ("object_radius", sphere_radius, "float"),
                                             ("importance_max", self.node_processor.node_max_importance, "float"),
                                             ('show_class', show_class, 'int')])
        self.sphere_render.set_uniform_labeled_data(options)

        self.sphere_render.set()

        render_setting_0(False)
        glDrawArrays(GL_POINTS, 0, node_count)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)

    @track_time
    def render_transparent(self, cam: Camera, sphere_radius: float = 0.03, options: Dict[str, float] = None,
                           show_class: int = 0):
        node_count: int = len(self.node_processor.nodes)

        near, far = self.grid.get_near_far_from_view(cam.view)
        self.transparent_render.set_uniform_data([("projection", cam.projection, "mat4"),
                                                  ("view", cam.view, "mat4"),
                                                  ("farthest_point_view_z", far, "float"),
                                                  ("nearest_point_view_z", near, "float"),
                                                  ("object_radius", sphere_radius, "float"),
                                                  ("importance_max", self.node_processor.node_max_importance, "float"),
                                                  ('show_class', show_class, 'int')])
        self.transparent_render.set_uniform_labeled_data(options)

        self.transparent_render.set()

        render_setting_1(False)
        glDrawArrays(GL_POINTS, 0, node_count)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)

    def delete(self):
        self.data_handler.delete()

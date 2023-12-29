from __future__ import annotations


from typing import (
    Iterator,
    Self
)

import moderngl

from ...animatables.animatable.animatable import Animatable
from ...animatables.arrays.animatable_color import AnimatableColor
from ...animatables.arrays.animatable_float import AnimatableFloat
from ...animatables.mesh import Mesh
from ...animatables.model import Model
from ...constants.custom_typing import (
    NP_3f8,
    NP_f8,
    NP_x2f8,
    NP_x3f8,
    NP_x3i4
)
from ...lazy.lazy import Lazy
from ...rendering.buffers.attributes_buffer import AttributesBuffer
from ...rendering.buffers.texture_buffer import TextureBuffer
from ...rendering.buffers.uniform_block_buffer import UniformBlockBuffer
from ...rendering.mgl_enums import PrimitiveMode
from ...rendering.vertex_array import VertexArray
from ...toplevel.toplevel import Toplevel
from ..mobject import Mobject


class MeshMobject(Mobject):
    __slots__ = ()

    def __init__(
        self: Self,
        mesh: Mesh | None = None
    ) -> None:
        super().__init__()
        if mesh is not None:
            self._mesh_ = mesh

    @Animatable.interpolate.register_descriptor()
    @Lazy.volatile()
    @staticmethod
    def _mesh_() -> Mesh:
        return Mesh()

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableColor)
    @Lazy.volatile()
    @staticmethod
    def _color_() -> AnimatableColor:
        return AnimatableColor(Toplevel._get_config().default_color)

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableFloat)
    @Lazy.volatile()
    @staticmethod
    def _opacity_() -> AnimatableFloat:
        return AnimatableFloat(Toplevel._get_config().default_opacity)

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableFloat)
    @Lazy.volatile()
    @staticmethod
    def _weight_() -> AnimatableFloat:
        return AnimatableFloat(Toplevel._get_config().default_weight)

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableFloat)
    @Lazy.volatile()
    @staticmethod
    def _ambient_strength_() -> AnimatableFloat:
        return AnimatableFloat(Toplevel._get_config().mesh_ambient_strength)

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableFloat)
    @Lazy.volatile()
    @staticmethod
    def _specular_strength_() -> AnimatableFloat:
        return AnimatableFloat(Toplevel._get_config().mesh_specular_strength)

    @Animatable.interpolate.register_descriptor()
    @Model.set.register_descriptor(converter=AnimatableFloat)
    @Lazy.volatile()
    @staticmethod
    def _shininess_() -> AnimatableFloat:
        return AnimatableFloat(Toplevel._get_config().mesh_shininess)

    @Lazy.variable(plural=True)
    @staticmethod
    def _color_maps_() -> tuple[moderngl.Texture, ...]:
        return ()

    @Lazy.property()
    @staticmethod
    def _local_sample_positions_(
        mesh__positions: NP_x3f8,
        mesh__faces: NP_x3i4
    ) -> NP_x3f8:
        return mesh__positions[mesh__faces.flatten()]

    @Lazy.property()
    @staticmethod
    def _color_maps_texture_buffer_(
        color_maps: tuple[moderngl.Texture, ...]
    ) -> TextureBuffer:
        return TextureBuffer(
            name="t_color_maps",
            textures=color_maps,
            array_lens={
                "NUM_T_COLOR_MAPS": len(color_maps)
            }
        )

    @Lazy.property()
    @staticmethod
    def _material_uniform_block_buffer_(
        color__array: NP_3f8,
        opacity__array: NP_f8,
        weight__array: NP_f8,
        ambient_strength__array: NP_f8,
        specular_strength__array: NP_f8,
        shininess__array: NP_f8
    ) -> UniformBlockBuffer:
        return UniformBlockBuffer(
            name="ub_material",
            field_declarations=(
                "vec3 u_color",
                "float u_opacity",
                "float u_weight",
                "float u_ambient_strength",
                "float u_specular_strength",
                "float u_shininess"
            ),
            data_dict={
                "u_color": color__array,
                "u_opacity": opacity__array,
                "u_weight": weight__array,
                "u_ambient_strength": ambient_strength__array,
                "u_specular_strength": specular_strength__array,
                "u_shininess": shininess__array
            }
        )

    @Lazy.property()
    @staticmethod
    def _mesh_attributes_buffer_(
        mesh__positions: NP_x3f8,
        mesh__normals: NP_x3f8,
        mesh__uvs: NP_x2f8,
        mesh__faces: NP_x3i4
    ) -> AttributesBuffer:
        return AttributesBuffer(
            field_declarations=(
                "vec3 in_position",
                "vec3 in_normal",
                "vec2 in_uv"
            ),
            data_dict={
                "in_position": mesh__positions,
                "in_normal": mesh__normals,
                "in_uv": mesh__uvs
            },
            index=mesh__faces.flatten(),
            primitive_mode=PrimitiveMode.TRIANGLES,
            vertices_count=len(mesh__positions)
        )

    @Lazy.property()
    @staticmethod
    def _mesh_vertex_array_(
        color_maps_texture_buffer: TextureBuffer,
        camera__camera_uniform_block_buffer: UniformBlockBuffer,
        lighting__lighting_uniform_block_buffer: UniformBlockBuffer,
        model_uniform_block_buffer: UniformBlockBuffer,
        material_uniform_block_buffer: UniformBlockBuffer,
        mesh_attributes_buffer: AttributesBuffer
    ) -> VertexArray:
        return VertexArray(
            shader_filename="mesh.glsl",
            texture_buffers=(
                color_maps_texture_buffer,
            ),
            uniform_block_buffers=(
                camera__camera_uniform_block_buffer,
                lighting__lighting_uniform_block_buffer,
                model_uniform_block_buffer,
                material_uniform_block_buffer
            ),
            attributes_buffer=mesh_attributes_buffer
        )

    def _iter_vertex_arrays(
        self: Self
    ) -> Iterator[VertexArray]:
        yield from super()._iter_vertex_arrays()
        yield self._mesh_vertex_array_

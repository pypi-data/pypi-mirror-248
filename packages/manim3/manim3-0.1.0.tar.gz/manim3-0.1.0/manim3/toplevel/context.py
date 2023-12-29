from __future__ import annotations


from typing import (
    Iterator,
    Self
)

import moderngl
import pyglet.gl as gl

from ..rendering.mgl_enums import (
    BlendEquation,
    BlendFunc,
    ContextFlag,
    PrimitiveMode
)
from .toplevel import Toplevel
from .toplevel_resource import ToplevelResource


class Context(ToplevelResource):
    __slots__ = ("_mgl_context",)

    def __init__(
        self: Self
    ) -> None:
        super().__init__()
        mgl_context = moderngl.create_context(
            require=Toplevel._get_config().gl_version_code
        )
        mgl_context.gc_mode = "auto"
        self._mgl_context: moderngl.Context = mgl_context

    def __contextmanager__(
        self: Self
    ) -> Iterator[None]:
        Toplevel._context = self
        yield
        Toplevel._context = None

    def set_blendings(
        self: Self,
        blendings: tuple[tuple[BlendFunc, BlendFunc, BlendEquation], ...]
    ) -> None:
        for index, (src_blend_func, dst_blend_func, blend_equation) in enumerate(blendings):
            gl.glBlendFunci(
                index,
                src_blend_func.value,
                dst_blend_func.value
            )
            gl.glBlendEquationi(
                index,
                blend_equation.value
            )

    def set_flag(
        self: Self,
        flag: ContextFlag
    ) -> None:
        self._mgl_context.enable_only(flag.value)

    @property
    def version_code(
        self: Self
    ) -> int:
        return self._mgl_context.version_code

    @property
    def screen_framebuffer(
        self: Self
    ) -> moderngl.Framebuffer:
        return self._mgl_context.screen

    def texture(
        self: Self,
        *,
        size: tuple[int, int],
        components: int,
        samples: int,
        dtype: str
    ) -> moderngl.Texture:
        return self._mgl_context.texture(
            size=size,
            components=components,
            samples=samples,
            dtype=dtype
        )

    def framebuffer(
        self: Self,
        *,
        color_attachments: tuple[moderngl.Texture, ...]
    ) -> moderngl.Framebuffer:
        return self._mgl_context.framebuffer(
            color_attachments=color_attachments
        )

    def buffer(
        self: Self,
        *,
        data: bytes
    ) -> moderngl.Buffer:
        return self._mgl_context.buffer(data=data)

    def program(
        self: Self,
        *,
        vertex_shader: str,
        fragment_shader: str | None = None,
        geometry_shader: str | None = None,
        tess_control_shader: str | None = None,
        tess_evaluation_shader: str | None = None,
        varyings: tuple[str, ...] = ()
    ) -> moderngl.Program:
        return self._mgl_context.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
            geometry_shader=geometry_shader,
            tess_control_shader=tess_control_shader,
            tess_evaluation_shader=tess_evaluation_shader,
            varyings=varyings
        )

    def vertex_array(
        self: Self,
        *,
        program: moderngl.Program,
        attributes_buffer: moderngl.Buffer,
        attributes_buffer_format_str: str,
        attribute_names: tuple[str, ...],
        index_buffer: moderngl.Buffer | None,
        mode: PrimitiveMode
    ) -> moderngl.VertexArray:
        content = []
        if attribute_names:
            content.append((attributes_buffer, attributes_buffer_format_str, *attribute_names))
        return self._mgl_context.vertex_array(
            program=program,
            content=content,
            index_buffer=index_buffer,
            index_element_size=4,
            mode=mode.value
        )

    def scope(
        self: Self,
        *,
        framebuffer: moderngl.Framebuffer | None = None,
        textures: tuple[tuple[moderngl.Texture, int], ...] = (),
        uniform_buffers: tuple[tuple[moderngl.Buffer, int], ...] = ()
    ) -> moderngl.Scope:
        return self._mgl_context.scope(
            framebuffer=framebuffer,
            textures=textures,
            uniform_buffers=uniform_buffers
        )

    def blit_framebuffer(
        self: Self,
        *,
        dst: moderngl.Framebuffer,
        src: moderngl.Framebuffer
    ) -> None:
        # Moderngl `copy_framebuffer` does not support unequal frame sizes.
        # This method is a simple patch for such requirement.
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, src.glo)
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, dst.glo)
        gl.glBlitFramebuffer(
            *src.viewport, *dst.viewport,
            gl.GL_COLOR_BUFFER_BIT, gl.GL_LINEAR
        )

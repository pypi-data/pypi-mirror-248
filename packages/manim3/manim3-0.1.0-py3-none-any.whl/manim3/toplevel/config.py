from __future__ import annotations


import pathlib
import sys
from typing import (
    Iterator,
    Self
)

import attrs
from colour import Color

from ..constants.custom_typing import ColorType
from .toplevel import Toplevel
from .toplevel_resource import ToplevelResource


@attrs.frozen(kw_only=True)
class Config(ToplevelResource):
    gl_version: tuple[int, int] = (4, 3)
    fps: int = 30
    aspect_ratio: float = 16.0 / 9.0
    frame_height: float = 8.0
    pixel_height: int = 1080
    window_pixel_height: int = 540
    msaa_samples: int = 4  # Set to 0 to disable msaa.

    default_color: ColorType = Color("white")
    default_opacity: float = 1.0
    default_weight: float = 1.0
    background_color: ColorType = Color("black")
    background_opacity: float = 0.0

    camera_distance: float = 5.0
    camera_near: float = 0.1
    camera_far: float = 100.0

    mesh_ambient_strength: float = 1.0
    mesh_specular_strength: float = 0.5
    mesh_shininess: float = 32.0
    graph_thickness: float = 0.05

    typst_preamble: str = ""
    typst_align: str | None = None
    typst_font: str | tuple[str, ...] | None = None
    math_inline: bool = False
    code_syntax: str = "py"
    code_theme: str | pathlib.Path | None = None

    shader_search_dirs: tuple[pathlib.Path, ...] = (
        pathlib.Path(),
        pathlib.Path(__import__("manim3").__file__).parent.joinpath("shaders")
    )
    image_search_dirs: tuple[pathlib.Path, ...] = (
        pathlib.Path(),
    )
    output_dir: pathlib.Path = pathlib.Path("manim3_output")
    video_output_dir: pathlib.Path = pathlib.Path("manim3_output/videos")
    image_output_dir: pathlib.Path = pathlib.Path("manim3_output/images")
    default_filename: str = sys.argv[0].removesuffix(".py")

    @property
    def gl_version_code(
        self: Self
    ) -> int:
        major_version, minor_version = self.gl_version
        return major_version * 100 + minor_version * 10

    @property
    def frame_size(
        self: Self
    ) -> tuple[float, float]:
        return self.aspect_ratio * self.frame_height, self.frame_height

    @property
    def pixel_size(
        self: Self
    ) -> tuple[int, int]:
        return int(self.aspect_ratio * self.pixel_height), self.pixel_height

    @property
    def window_pixel_size(
        self: Self
    ) -> tuple[int, int]:
        return int(self.aspect_ratio * self.window_pixel_height), self.window_pixel_height

    @property
    def pixel_per_unit(
        self: Self
    ) -> float:
        return self.pixel_height / self.frame_height

    def __contextmanager__(
        self: Self
    ) -> Iterator[None]:
        from .timer import Timer
        from .logger import Logger
        from .window import Window
        from .context import Context
        from .renderer import Renderer

        Toplevel._config = self
        with (
            Timer(),
            Logger(),
            Window(),
            Context(),
            Renderer()
        ):
            yield
        Toplevel._config = None

from __future__ import annotations


from typing import (
    Self,
    Unpack
)

import numpy as np

from ...animatables.animatable.animatable import Animatable
from ...animatables.mesh import Mesh
from ...animatables.model import SetKwargs
from ...animatables.shape import (
    Shape,
    Triangulation
)
from ...lazy.lazy import Lazy
from ..graph_mobjects.graph_mobject import GraphMobject
from ..mesh_mobjects.mesh_mobject import MeshMobject


class ShapeMobject(MeshMobject):
    __slots__ = ()

    def __init__(
        self: Self,
        shape: Shape | None = None
    ) -> None:
        super().__init__()
        if shape is not None:
            self._shape_ = shape

    @Animatable.interpolate.register_descriptor()
    @Animatable.piecewise.register_descriptor()
    @Lazy.volatile()
    @staticmethod
    def _shape_() -> Shape:
        return Shape()

    @Lazy.property()
    @staticmethod
    def _mesh_(
        shape__triangulation: Triangulation
    ) -> Mesh:
        coordinates = shape__triangulation.coordinates
        faces = shape__triangulation.faces
        positions = np.concatenate((coordinates, np.zeros((len(coordinates), 1))), axis=1)
        normals = np.concatenate((np.zeros_like(coordinates), np.ones((len(coordinates), 1))), axis=1)
        return Mesh(
            positions=positions,
            normals=normals,
            uvs=coordinates,
            faces=faces
        )

    def build_stroke(
        self: Self,
        **kwargs: Unpack[SetKwargs]
    ) -> GraphMobject:
        stroke = GraphMobject()
        stroke._model_matrix_ = self._model_matrix_.copy()
        stroke._graph_ = self._shape_._graph_.copy()
        stroke.set(**kwargs)
        return stroke

    def add_strokes(
        self: Self,
        **kwargs: Unpack[SetKwargs]
    ) -> Self:
        for mobject in self.iter_descendants():
            if isinstance(mobject, ShapeMobject):
                mobject.add(mobject.build_stroke(**kwargs))
        return self

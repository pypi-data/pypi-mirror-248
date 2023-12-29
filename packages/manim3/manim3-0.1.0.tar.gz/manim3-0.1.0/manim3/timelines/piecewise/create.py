from __future__ import annotations


from typing import Self

from ...animatables.animatable.piecewiser import Piecewiser
from ...mobjects.mobject import Mobject
from ..timeline import Timeline


class PartialPiecewiser(Piecewiser):
    __slots__ = ()

    def get_segment(
        self: Self,
        alpha: float
    ) -> tuple[float, float]:
        return (0.0, alpha)


class Create(Timeline):
    __slots__ = (
        "_mobject",
        "_piecewiser"
    )

    def __init__(
        self: Self,
        mobject: Mobject,
        *,
        n_segments: int = 1,
        backwards: bool = False
    ) -> None:
        super().__init__(run_alpha=1.0)
        self._mobject: Mobject = mobject
        self._piecewiser: PartialPiecewiser = PartialPiecewiser(
            n_segments=n_segments,
            backwards=backwards
        )

    async def construct(
        self: Self
    ) -> None:
        mobject = self._mobject

        self.scene.add(mobject)
        await self.play(mobject.animate().piecewise(mobject.copy(), self._piecewiser))

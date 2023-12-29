from __future__ import annotations


from typing import Self

from ...mobjects.mobject import Mobject
from ..timeline import Timeline


class Transform(Timeline):
    __slots__ = (
        "_start_mobject",
        "_stop_mobject"
    )

    def __init__(
        self: Self,
        start_mobject: Mobject,
        stop_mobject: Mobject
    ) -> None:
        super().__init__(run_alpha=1.0)
        self._start_mobject: Mobject = start_mobject
        self._stop_mobject: Mobject = stop_mobject

    async def construct(
        self: Self
    ) -> None:
        start_mobject = self._start_mobject
        stop_mobject = self._stop_mobject
        intermediate_mobject = start_mobject.copy()

        self.scene.discard(start_mobject)
        self.scene.add(intermediate_mobject)
        await self.play(intermediate_mobject.animate().interpolate(start_mobject, stop_mobject))
        self.scene.discard(intermediate_mobject)
        self.scene.add(stop_mobject)

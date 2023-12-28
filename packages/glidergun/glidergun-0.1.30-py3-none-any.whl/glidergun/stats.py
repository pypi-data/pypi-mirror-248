from scipy import stats
from typing import NamedTuple, Tuple
from glidergun.core import Grid, _batch, _focal


class StatsResult(NamedTuple):
    statistic: Grid
    pvalue: Grid


def focal_ttest_ind(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False, **kwargs
) -> StatsResult:
    def f(grids: Tuple[Grid, ...]):
        return _focal(
            lambda a: stats.ttest_ind(a[:, :, 0], a[:, :, 1], axis=2, **kwargs),
            buffer,
            circle,
            *grids,
        )

    result = _batch(f, buffer, grid1, grid2)
    return StatsResult(*result)


def focal_f_oneway(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False, **kwargs
) -> StatsResult:
    def f(grids: Tuple[Grid, ...]):
        return _focal(
            lambda a: stats.f_oneway(a[:, :, 0], a[:, :, 1], axis=2, **kwargs),
            buffer,
            circle,
            *grids,
        )

    result = _batch(f, buffer, grid1, grid2)
    return StatsResult(*result)

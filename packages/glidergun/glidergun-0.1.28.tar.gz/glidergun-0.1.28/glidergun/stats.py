import numpy as np
import warnings
from numpy import ndarray
from numpy.lib.stride_tricks import sliding_window_view
from scipy import stats
from typing import Any, Callable, NamedTuple
from glidergun.core import Grid, _mask, _pad, _standardize


def focal(func: Callable[[ndarray], Any], buffer: int, circle: bool, *grids: Grid):
    grids_adjusted = _standardize(True, *grids)
    size = 2 * buffer + 1
    mask = _mask(buffer) if circle else np.full((size, size), True)

    arrays = [
        sliding_window_view(_pad(g.data, buffer), (size, size)) for g in grids_adjusted
    ]

    data = np.transpose(np.stack(arrays), axes=(1, 2, 0, 3, 4))[:, :, :, mask]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = func(data)

    if isinstance(result, ndarray) and len(result.shape) == 2:
        return (grids_adjusted[0]._create(np.array(result)),)

    return tuple([grids_adjusted[0]._create(r) for r in result])


class StatsResult(NamedTuple):
    statistic: Grid
    pvalue: Grid


def focal_ttest_ind(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False, **kwargs
) -> StatsResult:
    result = focal(
        lambda a: stats.ttest_ind(a[:, :, 0], a[:, :, 1], axis=2, **kwargs),
        buffer,
        circle,
        grid1,
        grid2,
    )
    return StatsResult(*result)


def focal_f_oneway(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False, **kwargs
) -> StatsResult:
    result = focal(
        lambda a: stats.f_oneway(a[:, :, 0], a[:, :, 1], axis=2, **kwargs),
        buffer,
        circle,
        grid1,
        grid2,
    )
    return StatsResult(*result)

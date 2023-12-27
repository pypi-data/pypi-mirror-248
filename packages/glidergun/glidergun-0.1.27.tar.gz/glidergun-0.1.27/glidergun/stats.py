import numpy as np
import warnings
from numpy import ndarray
from numpy.lib.stride_tricks import sliding_window_view
from scipy import stats
from typing import Callable, List, NamedTuple
from glidergun.core import Grid, Value, _mask, _pad, _standardize


def focal(
    func: Callable[[List[ndarray]], List[Value]],
    buffer: int,
    circle: bool,
    *grids: Grid,
):
    grids_adjusted = _standardize(True, *grids)
    size = 2 * buffer + 1
    mask = _mask(buffer) if circle else None

    arrays = [
        sliding_window_view(_pad(g.data, buffer), (size, size)) for g in grids_adjusted
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        results = [
            [
                func([block if mask is None else block * mask for block in blocks])
                for blocks in row
            ]
            for row in np.array(arrays).transpose((1, 2, 0, 3, 4))
        ]

    return tuple(
        [
            grids_adjusted[0]._create(result)
            for result in np.transpose(np.array(results), axes=(2, 0, 1))
        ]
    )


def _values(data: ndarray):
    d = data.ravel()
    return d[np.isfinite(d)]


def _pearson(data: List[ndarray]):
    try:
        return [np.corrcoef(_values(data[0]), _values(data[1]))[0, 1]]
    except Exception:
        return [np.nan]


def focal_pearson(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False
) -> Grid:
    return focal(_pearson, buffer, circle, grid1, grid2)[0]


class TtestResult(NamedTuple):
    statistic: Grid
    pvalue: Grid


def _ttest(data: List[ndarray]):
    try:
        result = stats.ttest_ind(_values(data[0]), _values(data[1]))
        return [result[0], result[1]]
    except Exception:
        return [np.nan, np.nan]


def focal_ttest(
    grid1: Grid, grid2: Grid, buffer: int = 1, circle: bool = False
) -> TtestResult:
    result = focal(_ttest, buffer, circle, grid1, grid2)
    return TtestResult(*result)

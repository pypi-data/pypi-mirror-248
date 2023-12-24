import numpy as np
from numpy import ndarray
from scipy import stats
from typing import List, NamedTuple
from glidergun.core import focal, Grid


def _values(data: ndarray):
    d = data.ravel()
    return d[np.isfinite(d)]


class DescribeResult(NamedTuple):
    nobs: Grid
    min: Grid
    max: Grid
    mean: Grid
    variance: Grid
    skewness: Grid
    kurtosis: Grid


def _describe(data: List[ndarray]):
    try:
        result = stats.describe(_values(data[0]))
        return [
            result[0],
            result[1][0],
            result[1][1],
            result[2],
            result[3],
            result[4],
            result[5],
        ]
    except Exception:
        return [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]


def focal_describe(grid: Grid, buffer: int = 1, circle: bool = False) -> DescribeResult:
    result = focal(_describe, buffer, circle, grid)
    return DescribeResult(*result)


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

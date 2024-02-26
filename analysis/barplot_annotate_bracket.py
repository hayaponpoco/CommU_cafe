from __future__ import annotations
from typing import Any, Union, Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


RGBColorType = Union[tuple[float, float, float], str]
RGBAColorType = Union[
    str,  # "none" or "#RRGGBBAA"/"#RGBA" hex strings
    tuple[float, float, float, float],
    # 2 tuple (color, alpha) representations, not infinitely recursive
    # RGBColorType includes the (str, float) tuple, even for RGBA strings
    tuple[RGBColorType, float],
    # (4-tuple, float) is odd, but accepted as the outer float overriding A of 4-tuple
    tuple[tuple[float, float, float, float], float],
]

ColorType = Union[RGBColorType, RGBAColorType]
# https://github.com/matplotlib/matplotlib/blob/v3.8.2/lib/matplotlib/typing.py


ArrayLike = Union[list, tuple, np.ndarray, pd.Series]


def barplot_annotate_bracket(
        num1: int,
        num2: int,
        data: Any,
        center: ArrayLike,
        height: ArrayLike,
        yerr: Optional[ArrayLike] = None,
        dh: float = 0.05,
        barh: float = 0.05,
        pad: float = 0.01,
        color: Optional[ColorType] = 'black',
        linewidth: Optional[float] = None,
        fontsize: Optional[int | float] = None,
        ax: Optional[plt.Axes] = None
    ) -> None:
    """
    Annotate barplot with p-values.
    Modified from https://omedstu.jimdofree.com/2019/02/11/matplotlibで棒グラフ間の有意差の描画をする/ .

    Parameters
    ----------
    :param num1: Number of left bar to put bracket over.
    :param num2: Number of right bar to put bracket over.
    :param data: String to write or Number for generating asterixes.
    :param center: Centers of all bars (like `plt.bar()` input).
    :param height: Heights of all bars (like `plt.bar()` input).

    Other Parameters
    ----------------
    :param yerr: Yerrs of all bars (like `plt.bar()` input).
    :param dh: Height offset over bar / bar + yerr in axes coordinates (0 to 1).
    :param barh: Bar height in axes coordinates (0 to 1).
    :param pad: Distance between bracket and text in axes coordinates (0 to 1).
    :param color: Color of bracket and text.
    :param linewidth: Line width in points.
    :param fontsize: Font size.
    :param ax: Axes object to draw the plot onto, otherwise uses the current Axes.

    Notes
    -----
    Execute this function immediately after `matplotlib.pyplot.bar()` or `Axes.bar()`.

    `ArrayLike` contains `list`, `tuple`, `np.ndarray`, and `pd.Series`.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats

    ### main
    #### Generate toy data
    >>> np.random.seed(0)
    >>> x0 = np.random.normal(loc=1.9, scale=0.4, size=100)
    >>> x1 = np.random.normal(loc=2, scale=0.3, size=100)
    >>> x2 = np.random.normal(loc=2.5, scale=0.8, size=50)

    #### Welch’s t-test
    >>> t01_value, p01_value = stats.ttest_ind(x0, x1, equal_var=False)
    >>> t02_value, p02_value = stats.ttest_ind(x0, x2, equal_var=False)
    >>> t12_value, p12_value = stats.ttest_ind(x1, x2, equal_var=False)

    ### plot
    >>> heights = [np.mean(x0), np.mean(x1), np.mean(x2)]
    >>> std = [np.std(x0), np.std(x1), np.std(x2)]
    >>> label = ['x0', 'x1', 'x2']
    >>> width = 0.8  # the width of the bars
    >>> bars = np.arange(len(heights))
    >>> 
    >>> plt.figure(figsize=(4, 5))
    >>> plt.bar(
    ...     bars, heights, width, tick_label=label, yerr=std,
    ...     align='center', alpha=0.5, ecolor='black', capsize=5
    ... )
    >>> plt.ylim(0, 5)
    >>> barplot_annotate_bracket(
    ...     0, 1, p01_value,
    ...     bars, heights, yerr=std
    ... )
    >>> barplot_annotate_bracket(
    ...     0, 2, 'p < 0.001',
    ...     bars, heights, yerr=std
    ... )
    >>> barplot_annotate_bracket(
    ...     1, 2, p12_value,
    ...     bars, heights, yerr=std, dh=0.2
    ... )
    >>> plt.show()
    """

    if type(data) is str:
        text = data
    else:
        if data < 0.001:
            text = '***'
        elif data < 0.01:
            text = '**'
        elif data < 0.05:
            text = '*'
        else:
            text = 'n.s.'

    center = np.array(center)
    height = np.array(height)
    lx, ly = center[num1], height[num1]
    rx, ry = center[num2], height[num2]
    if yerr is not None:
        yerr = np.array(yerr)
        ly += yerr[num1]
        ry += yerr[num2]

    ax_y0, ax_y1 = plt.gca().get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= (ax_y1 - ax_y0)
    pad *= (ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, y+barh+pad)

    kwargs: dict[str, Any] = dict(c=color)
    if linewidth is not None:
        kwargs['linewidth'] = linewidth
    if ax is None:
        plt.plot(barx, bary, **kwargs)  # bracket
    else:
        ax.plot(barx, bary, **kwargs)   # bracket

    kwargs = dict(c=color, ha='center', va='bottom')
    if fontsize is not None:
        kwargs['fontsize'] = fontsize
    if ax is None:
        plt.text(*mid, text, **kwargs)  # text
    else:
        ax.text(*mid, text, **kwargs)   # text


if __name__ == '__main__':
    from scipy import stats

    """ main """
    # Generate toy data
    np.random.seed(0)
    x0 = np.random.normal(loc=1.9, scale=0.4, size=100)
    x1 = np.random.normal(loc=2, scale=0.3, size=100)
    x2 = np.random.normal(loc=2.5, scale=0.8, size=50)

    # Welch’s t-test
    t01_value, p01_value = stats.ttest_ind(x0, x1, equal_var=False)
    t02_value, p02_value = stats.ttest_ind(x0, x2, equal_var=False)
    t12_value, p12_value = stats.ttest_ind(x1, x2, equal_var=False)

    """ plot """
    heights = [np.mean(x0), np.mean(x1), np.mean(x2)]
    std = [np.std(x0), np.std(x1), np.std(x2)]
    label = ['x0', 'x1', 'x2']
    width = 0.8  # the width of the bars
    bars = np.arange(len(heights))

    plt.figure(figsize=(4, 5))
    plt.bar(
        bars, heights, width, tick_label=label, yerr=std,
        align='center', alpha=0.5, ecolor='black', capsize=5
    )
    plt.ylim(0, 5)
    barplot_annotate_bracket(
        0, 1, p01_value,
        bars, heights, yerr=std
    )
    barplot_annotate_bracket(
        0, 2, 'p < 0.001',
        bars, heights, yerr=std
    )
    barplot_annotate_bracket(
        1, 2, p12_value,
        bars, heights, yerr=std, dh=0.2
    )
    plt.show()

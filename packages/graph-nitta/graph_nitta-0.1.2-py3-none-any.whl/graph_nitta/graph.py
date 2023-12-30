import math
from typing import List, Optional, Tuple

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from graph_nitta.style.apply import apply_basic_style


def calc_grid(number_of_subplots: int) -> int:
    return math.ceil(math.sqrt(number_of_subplots))


def make_graph(
    number_of_subplots: int = 1, row: Optional[int] = None, column: Optional[int] = None
) -> Tuple[Figure, List[Axes]]:
    apply_basic_style()
    fig = plt.figure()
    grid = calc_grid(number_of_subplots)
    row = row or grid
    column = column or grid
    fig.set_size_inches(8 * column, 8 * row)
    axes = [fig.add_subplot(row, column, i + 1) for i in range(number_of_subplots)]
    return fig, axes

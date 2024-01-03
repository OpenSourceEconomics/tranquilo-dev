import matplotlib
import matplotlib.pyplot as plt
from tranquilo_dev.config import LABELS


# ======================================================================================
# Constants
# ======================================================================================
XAXIS_DEVIATION_PLOT = "Computational budget"
XAXIS_PROFILE_PLOT = "Computational budget (normalized)"

YAXIS_DEVIATION_PLOT = "Average distance to optimum (normalized)"
YAXIS_PROFILE_PLOT = "Share of solved problems"

FIGURE_WIDTH = 14.69785  # textwidth of paper in cm
FIGURE_HEIGHT = 10.0

AXIS_LABEL_COLOR = "#605752"

TABLEAU_10_COLORS = {
    "blue": "#5778a4",
    "orange": "#e49444",
    "red": "#d1615d",
    "teal": "#85b6b2",
    "green": "#6a9f58",
    "yellow": "#e7ca60",
    "purple": "#a87c9f",
    "pink": "#f1a2a9",
    "brown": "#967662",
    "gray": "#b8b0ac",
}


# ======================================================================================
# Global matplotlib settings
# ======================================================================================

matplotlib.rcParams["font.size"] = 10
matplotlib.rcParams["font.sans-serif"] = "Fira Sans"
matplotlib.rcParams["font.family"] = "sans-serif"


# ======================================================================================
# Profile plot updates
# ======================================================================================


def update_profile_plot_scalar_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 1, 50)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_PROFILE_PLOT, yname=YAXIS_PROFILE_PLOT)
    return fig


def update_profile_plot_ls_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 1, 40)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_PROFILE_PLOT, yname=YAXIS_PROFILE_PLOT)
    return fig


def update_profile_plot_parallel_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_PROFILE_PLOT, yname=YAXIS_PROFILE_PLOT)
    return fig


def update_profile_plot_noisy_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_PROFILE_PLOT, yname=YAXIS_PROFILE_PLOT)
    return fig


def update_profile_plot_scalar_vs_ls_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 1, 50)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_PROFILE_PLOT, yname=YAXIS_PROFILE_PLOT)
    return fig


# ======================================================================================
# Deviation plot updates
# ======================================================================================


def update_deviation_plot_scalar_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 0, 300)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_DEVIATION_PLOT, yname=YAXIS_DEVIATION_PLOT)
    return fig


def update_deviation_plot_ls_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 0, 400)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_DEVIATION_PLOT, yname=YAXIS_DEVIATION_PLOT)
    return fig


def update_deviation_plot_parallel_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 0, 50)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_DEVIATION_PLOT, yname=YAXIS_DEVIATION_PLOT)
    return fig


def update_deviation_plot_noisy_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_DEVIATION_PLOT, yname=YAXIS_DEVIATION_PLOT)
    return fig


def update_deviation_plot_scalar_vs_ls_benchmark(data):
    fig, ax = _create_base_plot(data)
    _update_xrange(ax, 0, 500)
    _update_legend(ax)
    _update_axes(ax, xname=XAXIS_DEVIATION_PLOT, yname=YAXIS_DEVIATION_PLOT)
    return fig


# ======================================================================================
# Shared functions
# ======================================================================================
def _create_base_plot(data):
    """Figure updates that are required by all plots."""
    # Update label names
    data = {LABELS[name]: line for name, line in data.items()}

    # Create matplotlib base figure
    fig, ax = plt.subplots(
        figsize=(_cm_to_inch(FIGURE_WIDTH), _cm_to_inch(FIGURE_HEIGHT))
    )
    for name, line in data.items():
        ax.plot(line["x"], line["y"], label=name)

    # Remove top and right border (spine)
    ax.spines[["right", "top"]].set_visible(False)

    # Update ticks
    ax.tick_params(direction="in", width=0.5)

    return fig, ax


def _update_xrange(ax, lower, upper):
    ax.set_xlim(lower, upper)


def _update_axes(ax, xname=None, yname=None):
    if xname is not None:
        ax.set_xlabel(xname, color=AXIS_LABEL_COLOR)
    if yname is not None:
        ax.set_ylabel(yname, color=AXIS_LABEL_COLOR)


def _update_legend(ax, ncol=3):
    ax.legend(
        frameon=False,
        loc="upper center",
        ncol=ncol,
        bbox_to_anchor=(0.5, -0.15),
        labelcolor=AXIS_LABEL_COLOR,
    )


def _cm_to_inch(cm):
    return cm * 0.393701

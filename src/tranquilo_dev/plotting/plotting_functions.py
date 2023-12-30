import plotly.graph_objects as go
from tranquilo_dev.config import LABELS


# ======================================================================================
# Constants
# ======================================================================================

XAXIS_NAME = "Computational Budget"
XAXIS_NAME_NORMALIZED = "Computational Budget (Normalized)"


# ======================================================================================
# Profile plot updates
# ======================================================================================


def update_profile_plot_scalar_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME_NORMALIZED)
    return fig


def update_profile_plot_ls_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 40)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME_NORMALIZED)
    return fig


def update_profile_plot_parallel_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME_NORMALIZED)
    return fig


def update_profile_plot_noisy_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME_NORMALIZED)
    return fig


def update_profile_plot_scalar_vs_ls_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME_NORMALIZED)
    return fig


# ======================================================================================
# Deviation plot updates
# ======================================================================================


def update_deviation_plot_scalar_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 300)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME)
    return fig


def update_deviation_plot_ls_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 400)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME)
    return fig


def update_deviation_plot_parallel_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME)
    return fig


def update_deviation_plot_noisy_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME)
    return fig


def update_deviation_plot_scalar_vs_ls_benchmark(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 500)
    fig = _update_axis_names(fig, xaxis=XAXIS_NAME)
    return fig


# ======================================================================================
# Shared functions
# ======================================================================================


def _update_xrange(fig, lower, upper):
    fig = go.Figure(fig)  # makes a copy of the figure
    fig.update_xaxes(range=[lower, upper])
    return fig


def _update_labels(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    for trace in fig.data:
        trace.update(name=LABELS[trace.name])
    return fig


def _update_axis_names(fig, xaxis=None, yaxis=None):
    fig = go.Figure(fig)  # makes a copy of the figure
    if xaxis is not None:
        fig.update_xaxes(title_text=xaxis)
    if yaxis is not None:
        fig.update_yaxes(title_text=yaxis)
    return fig


def _update_legend(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    fig.update_layout(
        legend_title=None,
        legend_orientation="h",
        legend_yanchor="top",
        legend_y=-0.5,
        legend_xanchor="center",
        legend_x=0.5,
    )
    return fig

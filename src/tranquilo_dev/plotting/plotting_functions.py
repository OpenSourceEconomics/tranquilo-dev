import plotly.graph_objects as go

LABELS = {
    "dfols": "DF-OLS",
    "tranquilo": "Tranquilo-Scalar",
    "tranquilo_default": "Tranquilo-Scalar",
    "tranquilo_ls_default": "Tranquilo-LS",
    "tranquilo_ls": "Tranquilo-LS",
    "nag_bobyqa": "NAG-BOBYQA",
    "nlopt_bobyqa": "NlOpt-BOBYQA",
    "nlopt_neldermead": "NlOpt-Nelder-Mead",
    "scipy_neldermead": "SciPy-Nelder-Mead",
    "tao_pounders": "TAO-Pounders",
    "pounders": "Pounders",
}


def update_scalar_benchmark_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    # cutoff xaxis range[0, 15]
    return fig


def update_ls_benchmark_plot(fig):
    # cutoff xaxis range[0, 40], is the red-line constant?
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    return fig


def update_parallel_benchmark_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_noisy_benchmark_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_scalar_vs_ls_benchmark_plot(fig):
    fig = _update_legend(fig)
    # cutoff xaxis range[0, 50]
    return fig


def _update_labels(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    for trace in fig.data:
        trace.update(name=LABELS[trace.name])
    return fig


def _update_legend(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    fig.update_layout(
        legend_title="Algorithm",
        legend_title_side="top",
    )
    return fig

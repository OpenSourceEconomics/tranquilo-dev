import plotly.io as pio
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.plotting.illustrations import create_noise_plots
from tranquilo_dev.plotting.illustrations import create_other_illustration_plots

pio.kaleido.scope.mathjax = None


BLD_SLIDEV = BLD.joinpath("bld_slidev")
BLD_PAPER = BLD.joinpath("bld_paper")

NOISE_PLOT_NAMES = [f"noise_plot_{k}.svg" for k in range(5)]

NOISE_PLOT_PRODUCES = []
for folder, suffix in ((BLD_SLIDEV, ".svg"), (BLD_PAPER / "illustrations", ".pdf")):
    for name in NOISE_PLOT_NAMES:
        NOISE_PLOT_PRODUCES.append(folder.joinpath(f"{name}").with_suffix(suffix))


@pytask.mark.produces(NOISE_PLOT_PRODUCES)
def task_create_noise_plots(produces):
    figures = create_noise_plots()
    # loop over (*figures, *figures) to write the same figure twice for svg and pdf
    for path, fig in zip(produces.values(), (*figures, *figures)):
        pio.full_figure_for_development(fig, warn=False)
        fig.write_image(path)


OTHER_ILLUSTRATION_NAMES = [
    *[f"animation_{k}.svg" for k in range(6)],
    *[f"line_points_{k}.svg" for k in range(1, 4)],
    "origin_plot.svg",
    "empty_speculative_trustregion_small_scale.svg",
    "empty_speculative_trustregion_large_scale.svg",
    "sampled_speculative_trustregion_small_scale.svg",
    "sampled_speculative_trustregion_large_scale.svg",
    "line_and_speculative_points.svg",
    "checklayout.svg",
]


@pytask.mark.produces([BLD_SLIDEV.joinpath(name) for name in OTHER_ILLUSTRATION_NAMES])
def task_create_other_illustration_plots(produces):
    figures = create_other_illustration_plots()
    for path in produces.values():
        figures[path.name].write_image(path)


ILLUSTRATION_PLOT_NAMES = NOISE_PLOT_NAMES + OTHER_ILLUSTRATION_NAMES

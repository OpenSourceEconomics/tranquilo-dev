import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.plotting.illustrations import create_noise_plots
from tranquilo_dev.plotting.illustrations import create_other_illustration_plots

BLD_SLIDEV = BLD.joinpath("bld_slidev")


@pytask.mark.produces({k: BLD_SLIDEV.joinpath(f"noise_plot_{k}.svg") for k in range(5)})
def task_create_noise_plots(produces):
    figures = create_noise_plots()
    for path, fig in zip(produces.values(), figures):
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

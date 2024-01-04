import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.plotting.illustrations import create_noise_plots

BLD_SLIDEV = BLD.joinpath("bld_slidev")


@pytask.mark.produces({k: BLD_SLIDEV.joinpath(f"noise_plot_{k}.svg") for k in range(5)})
def task_create_publication_noise_plots(produces):
    figures = create_noise_plots()
    for path, fig in zip(produces.values(), figures.values()):
        fig.write_image(path)

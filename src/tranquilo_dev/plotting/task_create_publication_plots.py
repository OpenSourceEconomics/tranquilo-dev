import estimagic as em
import pandas as pd
import pytask
from estimagic import profile_plot
from estimagic.visualization.deviation_plot import deviation_plot
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.plotting.plotting_functions import plot_benchmark


BLD_PAPER = BLD.joinpath("bld_paper")

ESTIMAGIC_PLOT_FUNCTIONS = {
    "profile_plot": profile_plot,
    "deviation_plot": deviation_plot,
}

for plot_type in ("profile_plot", "deviation_plot"):

    plot_func = ESTIMAGIC_PLOT_FUNCTIONS[plot_type]

    for benchmark in (
        "scalar_benchmark",
        "ls_benchmark",
        "parallel_benchmark",
        "noisy_benchmark",
        "scalar_vs_ls_benchmark",
    ):
        # Retrieve plotting info and function
        # ==============================================================================
        info = PLOT_CONFIG[f"publication_{benchmark}"]
        problem_name = info["problem_name"]
        plot_kwargs = info.get(f"{plot_type}_options", {})

        # Retrieve plotting data
        # ==============================================================================
        dependencies = [
            BLD.joinpath("benchmarks", f"{problem_name}_{scenario}.pkl")
            for scenario in info["scenarios"]
        ]
        problems = em.get_benchmark_problems(**PROBLEM_SETS[problem_name])

        # Store variables in kwargs to pass to pytask
        # ==============================================================================
        kwargs = {
            "plot_func": plot_func,
            "plot_kwargs": plot_kwargs,
            "problems": problems,
            "plot_type": plot_type,
            "benchmark": benchmark,
        }

        task_id = f"{plot_type}_{benchmark}"

        @pytask.mark.task(id=task_id, kwargs=kwargs)
        @pytask.mark.depends_on(dependencies)
        @pytask.mark.produces(BLD_PAPER.joinpath(f"{plot_type}s", f"{benchmark}.pdf"))
        def task_create_publication_plots(
            depends_on,
            produces,
            plot_func,
            plot_kwargs,
            problems,
            plot_type,
            benchmark,
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

            plotly_fig = plot_func(problems=problems, results=results, **plot_kwargs)
            plotting_data = get_data_from_plotly_figure(plotly_fig)

            fig = plot_benchmark(
                plotting_data,
                plot=plot_type,
                benchmark=benchmark,
            )
            fig.savefig(produces, bbox_inches="tight")


def get_data_from_plotly_figure(fig):
    lines = fig.data
    return {line.name: {"x": line.x, "y": line.y} for line in lines}

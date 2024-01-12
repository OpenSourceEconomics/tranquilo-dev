import pandas as pd
import pytask
from estimagic import convergence_plot
from estimagic import profile_plot
from estimagic.visualization.deviation_plot import deviation_plot
from tranquilo_dev.benchmarks.benchmark_problems import get_extended_benchmark_problems
from tranquilo_dev.config import BENCHMARK_PROBLEMS_INFO
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.plotting.benchmark_plotting_functions import plot_benchmark


# We store all figures used in the paper in a specific folder that is then copied
# entirely to the tranquilo-paper repository.
BLD_PAPER = BLD.joinpath("bld_paper")

ESTIMAGIC_PLOT_FUNCTIONS = {
    "profile_plot": profile_plot,
    "deviation_plot": deviation_plot,
    "convergence_plot": convergence_plot,
}

# ======================================================================================
# Publication ready figures
# ======================================================================================

for plot_type in ("profile_plot", "deviation_plot", "convergence_plot"):

    plot_func = ESTIMAGIC_PLOT_FUNCTIONS[plot_type]

    for benchmark, info in PLOT_CONFIG.items():

        # Retrieve plotting info and function
        # ==============================================================================
        problem_name = info["problem_name"]
        plot_kwargs = info.get(f"{plot_type}_options", {})

        # Retrieve plotting data
        # ==============================================================================
        dependencies = [
            BLD.joinpath("benchmarks", f"{problem_name}_{scenario}.pkl")
            for scenario in info["scenarios"]
        ]
        problems = get_extended_benchmark_problems(
            benchmark_kwargs=PROBLEM_SETS[problem_name], **BENCHMARK_PROBLEMS_INFO
        )

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

        if "publication_" in benchmark:
            _plot_name = benchmark.removeprefix("publication_")
            produces = BLD_PAPER / f"{plot_type}s" / f"{_plot_name}.pdf"
        elif "development_" in benchmark:
            _plot_name = benchmark.removeprefix("development_")
            produces = BLD / "figures" / f"{plot_type}s" / f"{_plot_name}.pdf"

        @pytask.mark.task(id=task_id, kwargs=kwargs)
        @pytask.mark.depends_on(dependencies)
        @pytask.mark.produces(produces)
        def task_create_benchmark_plots(
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
            plotting_data = _get_data_from_plotly_figure(plotly_fig)

            fig = plot_benchmark(
                plotting_data,
                plot=plot_type,
                benchmark=benchmark,
            )
            fig.savefig(produces, bbox_inches="tight")


def _get_data_from_plotly_figure(fig):
    lines = fig.data
    return {line.name: {"x": line.x, "y": line.y} for line in lines}

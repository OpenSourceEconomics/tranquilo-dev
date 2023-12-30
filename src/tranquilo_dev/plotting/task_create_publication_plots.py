import estimagic as em
import pandas as pd
import plotly.io as pio
import pytask
import tranquilo_dev.plotting.plotting_functions as plotting_functions
from estimagic import profile_plot
from estimagic.visualization.deviation_plot import deviation_plot
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS


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

        update_plot = getattr(plotting_functions, f"update_{plot_type}_{benchmark}")

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
            "update_plot": update_plot,
            "problems": problems,
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
            update_plot,
            problems,
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

            fig = plot_func(problems=problems, results=results, **plot_kwargs)
            updated = update_plot(fig)
            # Deactivate warnings, that could otherwise be printed on the figure
            pio.full_figure_for_development(fig, warn=False)
            updated.write_image(produces)

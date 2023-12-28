import estimagic as em
import pandas as pd
import pytask
import tranquilo_dev.plotting.plotting_functions as plotting_functions
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS


for plot_type in (
    "scalar_benchmark",
    "ls_benchmark",
    "parallel_benchmark",
    "noisy_benchmark",
    "scalar_vs_ls_benchmark",
):

    # Retrieve plotting info and function
    # ==================================================================================
    info = PLOT_CONFIG[f"publication_{plot_type}"]
    problem_name = info["problem_name"]
    plot_kwargs = info.get("profile_plot_options", {})

    update_plot = getattr(plotting_functions, f"update_{plot_type}_plot")

    # Retrieve plotting data
    # ==================================================================================
    dependencies = [
        BLD.joinpath("benchmarks", f"{problem_name}_{scenario}.pkl")
        for scenario in info["scenarios"]
    ]
    problems = em.get_benchmark_problems(**PROBLEM_SETS[problem_name])

    # Pass variables created in loop to function; otherwise they don't bind to the func.
    # ==================================================================================
    kwargs = {
        "plot_kwargs": plot_kwargs,
        "update_plot": update_plot,
        "problems": problems,
    }

    @pytask.mark.task(id=plot_type, kwargs=kwargs)
    @pytask.mark.depends_on(dependencies)
    @pytask.mark.produces(BLD.joinpath("figures", "publication", f"{plot_type}.eps"))
    def task_create_publication_plots(
        depends_on,
        produces,
        plot_kwargs,
        update_plot,
        problems,
    ):
        results = {}
        for path in depends_on.values():
            results = {**results, **pd.read_pickle(path)}

        fig = em.profile_plot(problems=problems, results=results, **plot_kwargs)
        updated = update_plot(fig)
        updated.write_image(produces)

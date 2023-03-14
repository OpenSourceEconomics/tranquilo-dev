import estimagic as em
import pandas as pd
import pytask
from estimagic import convergence_plot
from estimagic import profile_plot
from estimagic.visualization.deviation_plot import deviation_plot
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS


for name, info in PLOT_CONFIG.items():
    problem_name = info["problem_name"]
    DEPS = {}
    for scenario in info["scenarios"]:
        DEPS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"

    for plot_type in ["profile", "convergence", "deviation"]:

        OUT = BLD / "figures" / f"{plot_type}_plots"

        @pytask.mark.depends_on(DEPS)
        @pytask.mark.produces(OUT / f"{name}.svg")
        @pytask.mark.task(id=f"{plot_type}_plot_{name}")
        def task_create_benchmark_plots(
            depends_on, produces, info=info, plot_type=plot_type
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

            problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

            func_dict = {
                "profile": profile_plot,
                "convergence": convergence_plot,
                "deviation": deviation_plot,
            }

            plot_func = func_dict[plot_type]
            kwargs = info.get(f"{plot_type}_plot_options", {})

            fig = plot_func(
                problems=problems,
                results=results,
                **kwargs,
            )

            fig.write_image(produces)

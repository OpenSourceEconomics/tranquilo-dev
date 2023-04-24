from copy import deepcopy

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

    for plot_type in ["convergence", "profile", "deviation"]:

        plot_options = deepcopy(info).get(f"{plot_type}_plot_options", {})

        OUT = BLD / "figures" / f"{plot_type}_plots"

        @pytask.mark.depends_on(DEPS)
        @pytask.mark.produces(OUT / f"{name}.svg")
        @pytask.mark.task(id=f"{plot_type}_plot_{name}")
        def task_create_benchmark_plots(
            depends_on,
            produces,
            info=info,
            plot_type=plot_type,
            plot_options=plot_options,
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

            problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

            func_dict = {
                "convergence": convergence_plot,
                "profile": profile_plot,
                "deviation": deviation_plot,
            }

            plot_func = func_dict[plot_type]

            fig = plot_func(
                problems=problems,
                results=results,
                **plot_options,
            )

            fig.write_image(produces)

import estimagic as em
import pandas as pd
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import PROFILE_PLOTS


OUT = BLD / "figures" / "profile_plots"


for name, info in PROFILE_PLOTS.items():
    problem_name = info["problem_name"]
    DEPS = {}
    for scenario in info["scenarios"]:
        DEPS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"

    @pytask.mark.depends_on(DEPS)
    @pytask.mark.produces(OUT / f"{name}.png")
    @pytask.mark.task(id=name)
    def task_create_profile_plots(depends_on, produces, info=info):
        results = {}
        for path in depends_on.values():
            results = {**results, **pd.read_pickle(path)}

        problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

        fig = em.profile_plot(
            problems=problems,
            results=results,
            y_precision=info.get("y_precision"),
            x_precision=info.get("x_precision"),
        )

        fig.update_layout(height=600, width=800)

        fig.write_image(produces)

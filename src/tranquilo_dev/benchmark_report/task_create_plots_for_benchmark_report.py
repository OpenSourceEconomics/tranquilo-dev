import estimagic as em
import pandas as pd
import pytask
from estimagic import convergence_plot
from estimagic import profile_plot
from estimagic.visualization.deviation_plot import deviation_plot
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import SPHINX_STATIC_BLD


for name, info in PLOT_CONFIG.items():
    problem_name = info["problem_name"]
    DEPS = {}
    for scenario in info["scenarios"]:
        DEPS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"

    for plot_type in ["profile", "deviation"]:

        OUT = SPHINX_STATIC_BLD / "figures" / f"{plot_type}_plots"

        @pytask.mark.depends_on(DEPS)
        @pytask.mark.produces(OUT / f"{name}.svg")
        @pytask.mark.task(id=f"{plot_type}_plot_{name}")
        def task_create_profile_and_deviation_plots(
            depends_on, produces, info=info, plot_type=plot_type
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

            problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

            func_dict = {
                "profile": profile_plot,
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

    plot_type = "convergence"
    problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])
    OUT_DICT = {}
    for prob in problems.keys():
        OUT_DICT[prob] = (
            SPHINX_STATIC_BLD
            / "figures"  # noqa: W503
            / f"{plot_type}_plots"  # noqa: W503
            / f"{name}"  # noqa: W503
            / f"{prob}.svg"  # noqa: W503
        )

    @pytask.mark.depends_on(DEPS)
    @pytask.mark.produces(OUT_DICT)
    @pytask.mark.task(id=f"{plot_type}_plots_{name}")
    def task_create_convergence_plots(
        depends_on, produces, info=info, plot_type=plot_type
    ):
        results = {}
        for path in depends_on.values():
            results = {**results, **pd.read_pickle(path)}

        problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

        kwargs = info.get(f"{plot_type}_plot_options", {})
        kwargs["combine_plots_in_grid"] = False

        figs = convergence_plot(
            problems=problems,
            results=results,
            **kwargs,
        )

        for key, fig in figs.items():
            fig.write_image(produces[key])

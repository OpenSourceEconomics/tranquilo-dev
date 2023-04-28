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

LINE_SETTINGS = {"parallelization_ls": {}, "noisy_ls": {}, "scalar_and_ls": {}}

tranquilo_scenarios = [
    sc for sc in PLOT_CONFIG["parallelization_ls"]["scenarios"] if "tranquilo" in sc
]
tranquilo_scenarios = sorted(tranquilo_scenarios, key=lambda x: int(x.split("_")[-1]))

competitor = [
    sc
    for sc in PLOT_CONFIG["parallelization_ls"]["scenarios"]
    if sc not in tranquilo_scenarios
][0]
LINE_SETTINGS["parallelization_ls"][competitor] = {
    "line": {"color": "#e53935", "dash": "solid"},
}


alphas = [0.38, 0.6, 1]

for i, scenario in enumerate(tranquilo_scenarios):
    LINE_SETTINGS["parallelization_ls"][scenario] = {
        "line": {"color": "#014683", "dash": "solid"},
        "opacity": alphas[i],
    }
dfols_scenarios = [sc for sc in PLOT_CONFIG["noisy_ls"]["scenarios"] if "dfols" in sc]
dfols_scenarios = sorted(dfols_scenarios, key=lambda x: int(x.split("_")[-1]))

tranquilo_noisy = [
    sc for sc in PLOT_CONFIG["noisy_ls"]["scenarios"] if sc not in dfols_scenarios
][0]
LINE_SETTINGS["noisy_ls"][tranquilo_noisy] = {
    "line": {"color": "#014683", "dash": "solid"},
}

for i, scenario in enumerate(dfols_scenarios):
    LINE_SETTINGS["noisy_ls"][scenario] = {
        "line": {"color": "#e53935", "dash": "solid"},
        "opacity": alphas[i],
    }
LINE_SETTINGS["scalar_and_ls"]["dfols"] = {
    "line": {"color": "#e53935", "dash": "solid"}
}

LINE_SETTINGS["scalar_and_ls"]["tranquilo_default"] = {
    "line": {"color": "#014683", "dash": "solid"},
    "opacity": 0.6,
}

LINE_SETTINGS["scalar_and_ls"]["tranquilo_ls_default"] = {
    "line": {"color": "#014683", "dash": "solid"},
}
LINE_SETTINGS["scalar_and_ls"]["nlopt_bobyqa"] = {
    "line": {"color": "green", "dash": "solid"},
}
LINE_SETTINGS["scalar_and_ls"]["nlopt_neldermead"] = {
    "line": {"color": "orange", "dash": "solid"},
}


for name, info in PLOT_CONFIG.items():

    problem_name = info["problem_name"]
    DEPS = {}
    for scenario in info["scenarios"]:
        DEPS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"

    for plot_type in ["convergence", "profile", "deviation"]:

        plot_options = deepcopy(info).get(f"{plot_type}_plot_options", {})

        problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

        OUT = {plot_type: BLD / "figures" / f"{plot_type}_plots" / f"{name}.svg"}
        if plot_type == "convergence":
            for problem in problems.keys():
                OUT[problem] = (
                    BLD
                    / "figures"  # noqa: W503
                    / f"{plot_type}_plots"  # noqa: W503
                    / f"{name}"  # noqa: W503
                    / f"{problem}.svg"  # noqa: W503
                )

        @pytask.mark.depends_on(DEPS)
        @pytask.mark.produces(OUT)
        @pytask.mark.task(id=f"{plot_type}_plot_{name}")
        def task_create_benchmark_plots(
            depends_on,
            produces,
            plot_type=plot_type,
            plot_options=plot_options,
            problems=problems,
            name=name,
        ):
            results = {}
            for path in depends_on.values():
                results = {**results, **pd.read_pickle(path)}

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
            if plot_type == "profile" and name in [
                "parallelization_ls",
                "noisy_ls",
                "scalar_and_ls",
            ]:

                for trace_name, kwargs in LINE_SETTINGS[name].items():
                    for trace in fig.data:

                        if trace.name == trace_name:
                            trace.update(kwargs)
                if name == "scalar_and_ls":
                    fig.update_xaxes(range=[trace.x[0], trace.x[-8]])
            fig.write_image(produces[plot_type])

            if plot_type == "convergence":
                plot_options["combine_plots_in_grid"] = False
                fig_dict = convergence_plot(
                    problems=problems,
                    results=results,
                    **plot_options,
                )
                for prob, fig in fig_dict.items():
                    fig.write_image(produces[prob])

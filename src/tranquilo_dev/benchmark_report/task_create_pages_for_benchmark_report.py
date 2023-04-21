import estimagic as em
import numpy as np
import pandas as pd
import pytask
import snakemd
from estimagic.benchmarking.process_benchmark_results import (
    create_convergence_histories,
)
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import SPHINX_PAGES_BLD
from tranquilo_dev.config import SPHINX_STATIC_BLD

for name, info in PLOT_CONFIG.items():

    problem_name = info["problem_name"]
    DEPS_RESULTS = {}
    DEPS_FIGURES = {}
    for scenario in info["scenarios"]:
        DEPS_RESULTS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"
    for plot_type in ["profile", "deviation"]:
        DEPS_FIGURES[plot_type] = (
            SPHINX_STATIC_BLD / "figures" / f"{plot_type}_plots" / f"{name}.svg"
        )

    @pytask.mark.depends_on(DEPS_FIGURES | DEPS_RESULTS)
    @pytask.mark.produces(SPHINX_PAGES_BLD / f"{name}.md")
    @pytask.mark.task(id=name)
    def task_create_benchmark_reports(
        name=name, info=info, path_to_results=DEPS_RESULTS
    ):
        doc = snakemd.new_doc()
        doc.add_heading(f"{name}", level=1)

        # 1. Profile and Deviation Plots
        for plot_type in ["profile", "deviation"]:
            doc.add_heading(f"{plot_type.capitalize()} Plot", level=2)
            doc.add_raw(
                f"![{plot_type}](../_static/bld/figures/{plot_type}_plots/{name}.svg)"
            )

        # 2. Convergence report
        df_out, converged_info, df_tracebacks, rank_report = _get_convergence_info(
            info=info, path_to_results=path_to_results
        )
        doc.add_heading("Convergence Report", level=2)
        rows_con = df_out.reset_index().values.tolist()
        header_con = ["problem"] + info["scenarios"] + ["dimensionality"]
        doc.add_table(header_con, rows_con)

        # 3. Rank report
        doc.add_heading("Rank Report", level=2)
        rows = rank_report.reset_index().values.tolist()
        header = ["problem"] + info["scenarios"]
        doc.add_table(header, rows)

        # 4. Error messages, grouped by scenario
        if len(df_tracebacks) > 0:
            doc.add_heading("Traceback Report", level=2)
            for scenario in df_tracebacks:
                if not df_tracebacks[scenario].isnull().any():
                    doc.add_heading(scenario, level=3)
                    tracebacks = df_tracebacks[scenario].to_dict()
                    for problem in tracebacks.keys():
                        traceback = tracebacks[problem]
                        doc.add_heading(problem, level=4)
                        doc.add_raw(f"```python \n{traceback} \n```")

        # 5. Convergence plots of all problems that have not been solved by tranquilo
        tranquilo_scenarios = [
            col for col in converged_info.columns if "tranquilo" in col
        ]
        doc.add_heading(
            "Convergence Plots for Problems Not Solved by tranquilo", level=2
        )
        for scenario in tranquilo_scenarios:
            doc.add_heading(scenario, level=3)
            problems_not_solved = converged_info.index[
                converged_info[scenario] == False  # noqa: E712
            ].tolist()
            for problem in problems_not_solved:
                doc.add_raw(
                    f"![convergence_{problem}]"
                    f"(../_static/bld/figures/convergence_plots/{name}/{problem}.svg)"
                )

        doc.dump(SPHINX_PAGES_BLD / name)


def _get_convergence_info(info, path_to_results):
    results = {}
    for path in path_to_results.values():
        results = {**results, **pd.read_pickle(path)}
    problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])

    options = info["profile_plot_options"]
    y_precision = options["y_precision"] if "y_precision" in options.keys() else None
    x_precision = options["x_precision"] if "x_precision" in options.keys() else None

    if y_precision and not x_precision:
        stopping_criterion = "y"
    elif x_precision and not y_precision:
        stopping_criterion = "x"
    elif y_precision and x_precision:
        stopping_criterion = "x_and_y"
    else:
        raise NotImplementedError(  # noqa: TC003
            "Either y_precision or x_precision (or both)" "must be specified."
        )

    df, converged_info = create_convergence_histories(
        problems=problems,
        results=results,
        stopping_criterion=stopping_criterion,
        x_precision=x_precision,
        y_precision=y_precision,
    )

    runtime_measure = "walltime"
    solution_times = df.groupby(["problem", "algorithm"])[runtime_measure].max()
    solution_times = solution_times.reset_index()
    solution_times = solution_times.sort_values(["problem", runtime_measure])
    solution_times["rank"] = np.tile(
        np.arange(len(info["scenarios"]), dtype=int), len(problems)
    )
    df_wide = solution_times.pivot(index="problem", columns="algorithm", values="rank")
    df_wide[~converged_info] = 999
    rank_report = df_wide[info["scenarios"]]

    df_out = converged_info.replace({True: "success", False: "failed"})

    tracebacks = {}
    for scenario in info["scenarios"]:
        tracebacks[scenario] = {}

    for key, value in results.items():
        if isinstance(value["solution"], str):
            df_out.at[key] = "error"
            tracebacks[key[1]][key[0]] = value["solution"]

    df_tracebacks = pd.DataFrame.from_dict(tracebacks, orient="columns")

    dim = {problem: len(problems[problem]["inputs"]["params"]) for problem in problems}
    df_out["dimensionality"] = df_out.index.map(dim)

    return df_out, converged_info, df_tracebacks, rank_report


def _create_rank_report():
    pass

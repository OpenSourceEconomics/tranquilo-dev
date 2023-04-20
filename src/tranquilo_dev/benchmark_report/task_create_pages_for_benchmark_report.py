import estimagic as em
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
        df_out, converged_info, df_tracebacks = _get_convergence_info(
            info=info, path_to_results=path_to_results
        )
        doc.add_heading("Convergence Report", level=2)
        rows_con = df_out.reset_index().values.tolist()
        header_con = ["problem"] + info["scenarios"] + ["dimensionality"]
        doc.add_table(header_con, rows_con)

        # 3. Rank report

        # 4. Error messages, grouped by scenario
        if len(df_tracebacks) > 0:
            doc.add_heading("Traceback Report", level=2)
            for scenario in df_tracebacks:
                if not df_tracebacks[scenario].isnull().any():
                    doc.add_heading(scenario, level=3)
                    rows = df_tracebacks[scenario].reset_index().values.tolist()
                    header = ["problem", "traceback"]
                    doc.add_table(header, rows)

        # 5. Convergence plots of all problems that have not been solved by tranquilo
        tranquilo_scenarios = [
            col for col in converged_info.columns if "tranquilo" in col
        ]
        doc.add_heading(
            "Convergence Plots of Problems Not Solved by tranquilo", level=2
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

    options = info["profile_plot_options"].keys()
    if "y_precision" in options and "x_precision" not in options:
        stopping_criterion = "y"
        x_precision = None
        y_precision = info["profile_plot_options"]["y_precision"]

    _, converged_info = create_convergence_histories(
        problems=problems,
        results=results,
        stopping_criterion=stopping_criterion,
        x_precision=x_precision,
        y_precision=y_precision,
    )

    # TO-DO: sort by wall time

    boolean_to_string = {True: "success", False: "failed"}
    df_out = converged_info.replace(boolean_to_string)

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

    return df_out, converged_info, df_tracebacks


def _create_rank_report():
    pass

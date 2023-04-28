import estimagic as em
import pandas as pd
import pytask
import snakemd
from estimagic.benchmarking.process_benchmark_results import (
    process_benchmark_results,
)
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import SPHINX_PAGES_BLD
from tranquilo_dev.config import SPHINX_STATIC_BLD


for name, info in PLOT_CONFIG.items():

    problem_name = info["problem_name"]
    problems = em.get_benchmark_problems(**PROBLEM_SETS[problem_name])

    DEPS_RESULTS = {}
    DEPS_FIGURES = {}
    for scenario in info["scenarios"]:
        DEPS_RESULTS[scenario] = BLD / "benchmarks" / f"{problem_name}_{scenario}.pkl"
        for problem in problems.keys():
            DEPS_FIGURES["convergence"] = (
                SPHINX_STATIC_BLD
                / "figures"  # noqa: W503
                / "convergence_plots"  # noqa: W503
                / f"{name}"  # noqa: W503
                / f"{problem}.svg"  # noqa: W503
            )
    for plot_type in ["profile", "deviation"]:
        DEPS_FIGURES[plot_type] = (
            SPHINX_STATIC_BLD / "figures" / f"{plot_type}_plots" / f"{name}.svg"
        )

    @pytask.mark.depends_on(DEPS_FIGURES | DEPS_RESULTS)
    @pytask.mark.produces(SPHINX_PAGES_BLD / f"{name}.md")
    @pytask.mark.task(id=f"markdown_page_{name}")
    def task_create_markdown_pages(
        produces,
        name=name,
        info=info,
        problems=problems,
        paths=DEPS_RESULTS,
    ):
        scenarios = info["scenarios"]
        results = {}
        for path in paths.values():
            results = {**results, **pd.read_pickle(path)}

        convergence_report = _create_convergence_report(
            problems=problems,
            results=results,
            **info.get("convergence_report_options", {}),
        )
        rank_report = _create_rank_report(
            problems=problems,
            results=results,
            **info.get("rank_report_options", {}),
        )
        traceback_report = _create_traceback_report(
            results=results,
        )

        doc = snakemd.new_doc()
        doc.add_heading(f"{name}", level=1)

        # 1. Profile and Deviation Plots
        for plot_type in ["profile", "deviation"]:
            doc.add_heading(f"{plot_type.capitalize()} Plot", level=2)
            doc.add_raw(
                f"![{plot_type}](../_static/bld/figures/{plot_type}_plots/{name}.svg)"
            )

        # 2. Convergence report
        doc.add_heading("Convergence Report", level=2)
        rows = convergence_report.reset_index().values.tolist()
        header = ["problem"] + info["scenarios"] + ["dimensionality"]
        doc.add_table(header, rows)

        # 3. Rank report
        doc.add_heading("Rank Report", level=2)
        rows = rank_report.reset_index().values.tolist()
        header = ["problem"] + info["scenarios"]
        doc.add_table(header, rows)

        # 4. Error messages, grouped by scenario
        if len(traceback_report) > 0:
            doc.add_heading("Traceback Report", level=2)
            for scenario in traceback_report:
                if not traceback_report[scenario].isnull().all():
                    doc.add_heading(scenario, level=3)
                    tracebacks = traceback_report[scenario].to_dict()
                    for problem, traceback in tracebacks.items():
                        if isinstance(traceback, str):
                            doc.add_heading(problem, level=4)
                            doc.add_raw(f"```python \n{traceback} \n```")

        # 5. Convergence plots of problems that have not been solved
        problems_not_solved = _get_problems_not_solved(
            problems=problems,
            results=results,
        )

        doc.add_heading("Convergence Plots for Problems Not Solved", level=2)
        for scenario in scenarios:
            doc.add_heading(scenario, level=3)
            for problem in problems_not_solved:
                doc.add_raw(
                    f"![convergence_{problem}]"
                    f"(../_static/bld/figures/convergence_plots/{name}/{problem}.svg)"
                )

        doc.dump(produces.parent / name)


def _create_convergence_report(
    problems, results, *, stopping_criterion="y", x_precision=1e-4, y_precision=1e-4
):
    """Create a DataFrame with all information needed for the convergence report.

    Args:
        problems (dict): estimagic benchmarking problems dictionary. Keys are the
            problem names. Values contain information on the problem, including the
            solution value.
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.
        stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y". Determines
            how convergence is determined from the two precisions. Default is "y".
        x_precision (float or None): how close an algorithm must have gotten to the
            true parameter values (as percent of the Euclidean distance between start
            and solution parameters) before the criterion for clipping and convergence
            is fulfilled. Default is 1e-4.
        y_precision (float or None): how close an algorithm must have gotten to the
            true criterion values (as percent of the distance between start
            and solution criterion value) before the criterion for clipping and
            convergence is fulfilled. Default is 1e-4.

    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms) and the
            dimensionality of the problems, index are the problems.
            For the scenario columns, the values are strings that are either
            "success" "failed", or "error". For the dimensionality column, the values
            denote the number dimensions of the problem.

    """
    _, converged_info = process_benchmark_results(
        problems=problems,
        results=results,
        stopping_criterion=stopping_criterion,
        x_precision=x_precision,
        y_precision=y_precision,
    )

    convergence_report = converged_info.replace({True: "success", False: "failed"})

    for key, value in results.items():
        if isinstance(value["solution"], str):
            convergence_report.at[key] = "error"

    dim = {problem: len(problems[problem]["inputs"]["params"]) for problem in problems}
    convergence_report["dimensionality"] = convergence_report.index.map(dim)

    return convergence_report


def _create_rank_report(
    problems,
    results,
    *,
    runtime_measure="n_evaluations",
    normalize_runtime=False,
    stopping_criterion="y",
    x_precision=1e-4,
    y_precision=1e-4,
):
    """Create a DataFrame with all information needed for the rank report.

    Args:
        problems (dict): estimagic benchmarking problems dictionary. Keys are the
            problem names. Values contain information on the problem, including the
            solution value.
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.
        runtime_measure (str): "n_evaluations", "n_batches" or "walltime".
            This is the runtime until the desired convergence was reached by an
            algorithm. This is called performance measure by Moré and Wild (2009).
            Default is "n_evaluations".
        normalize_runtime (bool): If True the runtime each algorithm needed for each
            problem is scaled by the time the fastest algorithm needed. If True, the
            resulting plot is what Moré and Wild (2009) called data profiles.
            Default is False.
        stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y". Determines
            how convergence is determined from the two precisions.
        x_precision (float or None): how close an algorithm must have gotten to the
            true parameter values (as percent of the Euclidean distance between start
            and solution parameters) before the criterion for clipping and convergence
            is fulfilled. Default is 1e-4.
        y_precision (float or None): how close an algorithm must have gotten to the
            true criterion values (as percent of the distance between start
            and solution criterion value) before the criterion for clipping and
            convergence is fulfilled. Default is 1e-4.

    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms), index are the
            problems. The values are the ranks of the algorithms for each problem,
            0 means the algorithm was the fastest, 1 means it was the second fastest
            and so on. If an algorithm did not converge on a problem, the value is
            "failed". If an algorithm did encounter an error during optimization,
            the value is "error".

    """
    histories, converged_info = process_benchmark_results(
        problems=problems,
        results=results,
        stopping_criterion=stopping_criterion,
        x_precision=x_precision,
        y_precision=y_precision,
    )
    scenarios = list({algo[1] for algo in results.keys()})

    success_info = converged_info.replace({True: "success", False: "failed"})
    for key, value in results.items():
        if isinstance(value["solution"], str):
            success_info.at[key] = "error"

    solution_times = histories.groupby(["problem", "algorithm"])[runtime_measure].max()

    if normalize_runtime:
        solution_times = solution_times.unstack()
        solution_times = solution_times.divide(solution_times.min(axis=1), axis=0)
        solution_times = solution_times.stack(dropna=False)
        solution_times.name = runtime_measure

    solution_times = solution_times.reset_index()
    solution_times["rank"] = (
        solution_times.groupby("problem")[runtime_measure].rank(
            method="dense", ascending=True
        )
        - 1  # noqa: W503
    ).astype("Int64")

    df_wide = solution_times.pivot(index="problem", columns="algorithm", values="rank")
    rank_report = df_wide.astype(str)[scenarios]
    rank_report[~converged_info] = success_info[scenarios]

    return rank_report


def _create_traceback_report(results):
    """Create a DataFrame with the traceback of all problems that have not been solved.

    Args:
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.

    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms), index are the
            problems. The values are the traceback of the algorithms for each problem
            the algorithm stopped with an error.

    """
    scenarios = list({algo[1] for algo in results.keys()})

    tracebacks = {}
    for scenario in scenarios:
        tracebacks[scenario] = {}

    for key, value in results.items():
        if isinstance(value["solution"], str):
            if key[1] in scenarios:
                tracebacks[key[1]][key[0]] = value["solution"]

    traceback_report = pd.DataFrame.from_dict(tracebacks, orient="columns")

    return traceback_report


def _get_problems_not_solved(problems, results, stopping_criterion="y"):
    """Get a list of problems that have not been solved by any algorithm.

    Args:
        problems (dict): estimagic benchmarking problems dictionary. Keys are the
            problem names. Values contain information on the problem, including the
            solution value.
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.
        stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y". Determines
            how convergence is determined from the two precisions. Default is "y".

    Returns:
        list: list of problem names that have not been solved by any algorithm.

    """
    kwargs = info.get("convergence_report_options", {})
    kwargs["stopping_criterion"] = kwargs.get("stopping_criterion", stopping_criterion)

    _, converged_info = process_benchmark_results(
        problems=problems,
        results=results,
        **kwargs,
    )

    problems_not_solved = converged_info.index[~converged_info.any(axis=1)].tolist()

    return problems_not_solved
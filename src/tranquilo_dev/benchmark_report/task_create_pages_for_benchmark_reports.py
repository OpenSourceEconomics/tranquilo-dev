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
    name = "competition_ls"
    problem_name = info["problem_name"]
    problems = em.get_benchmark_problems(**PROBLEM_SETS[problem_name])

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
    def task_create_pages(name=name, info=info, problems=problems, paths=DEPS_RESULTS):
        scenarios = info["scenarios"]
        options = _process_report_options_and_set_defaults(info["report_options"])
        (
            converged_info,
            convergence_report,
            rank_report,
            traceback_report,
        ) = _create_reports(
            problems=problems,
            scenarios=scenarios,
            options=options,
            paths=paths,
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

        # 5. Convergence plots of all problems that have not been solved
        if options["include_all_non_converged"]:
            convergence_scenarios = scenarios
        else:
            convergence_scenarios = [s for s in scenarios if "tranquilo" in s]
        doc.add_heading(
            "Convergence Plots for Problems Not Solved by tranquilo", level=2
        )
        for scenario in convergence_scenarios:
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


def _create_reports(problems, scenarios, options, paths):
    """Create all reports for a given benchmarking competition.

    Args:
        problems (dict): estimagic benchmarking problems dictionary. Keys are the
            problem names. Values contain information on the problem, including the
            solution value.
        scenarios (list): list of the names of the algorithms that should be included
            in the report.
        options (dict): dictionary with the following keys:
            - stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y".
                Determines how convergence is determined from the two precisions.
            - x_precision (float or None): how close an algorithm must have gotten to
                the true parameter values (as percent of the Euclidean distance between
                start and solution parameters) before the criterion for clipping and
                convergence is fulfilled.
            - y_precision (float or None): how close an algorithm must have gotten to
                the true criterion values (as percent of the distance between start
                and solution criterion value) before the criterion for clipping and
                convergence is fulfilled.
            - runtime_measure (str): "n_evaluations", "n_batches" or "walltime".
            - normalize_runtime (bool): If True the runtime each algorithm needed for
                each problem is scaled by the time the fastest algorithm needed. If
                True, the resulting plot is what Moré and Wild (2009) called data
                profiles.
            - include_all_tracebacks (bool): If True, all tracebacks of all scenarios
                are included in the traceback report. If False, only tracebacks of the
                tranquilo algorithms are included.
            - include_all_non_converged (bool): If True, all convergence plots of all
                algorithms that have not converged on a problem are included in the
                convergence report. If False, only problems that have not been solved
                by tranquilo are included.
        paths (dict): Nested dictionary with the paths to the pickled benchmarking
            results.

    Returns:
        tuple: Tuple of four pandas DataFrames with the convergence information,
            the convergence report, the rank report and the traceback report.

    """
    results = {}
    for path in paths.values():
        results = {**results, **pd.read_pickle(path)}

    df, _converged_info = create_convergence_histories(
        problems=problems,
        results=results,
        stopping_criterion=options["stopping_criterion"],
        x_precision=options["x_precision"],
        y_precision=options["y_precision"],
    )
    converged_info = _converged_info[scenarios]

    convergence_report = _create_convergence_report(
        converged_info, problems, results=results
    )

    rank_report = _create_rank_report(
        df=df,
        converged_info=converged_info,
        convergence_report=convergence_report,
        scenarios=scenarios,
        runtime_measure=options["runtime_measure"],
        normalize_runtime=options["normalize_runtime"],
    )

    traceback_report = _create_traceback_report(results, scenarios, options)

    return converged_info, convergence_report, rank_report, traceback_report


def _create_convergence_report(converged_info, problems, results):
    """Create a DataFrame with all information needed for the convergence report.

    Args:
        converged_info (pandas.DataFrame): columns are the algorithms, index are the
            problems. The values are boolean and True when the algorithm arrived at
            the solution with the desired precision.
        problems (dict): estimagic benchmarking problems dictionary. Keys are the
            problem names. Values contain information on the problem, including the
            solution value.
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.


    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms) and the
            dimensionality of the problems, index are the problems.
            For the scenario columns, the values are strings that are either
            "success" "failed", or "error". For the dimensionality column, the values
            denote the number dimensions of the problem.

    """
    convergence_report = converged_info.replace({True: "success", False: "failed"})

    for key, value in results.items():
        if isinstance(value["solution"], str):
            convergence_report.at[key] = "error"

    dim = {problem: len(problems[problem]["inputs"]["params"]) for problem in problems}
    convergence_report["dimensionality"] = convergence_report.index.map(dim)

    return convergence_report


def _create_rank_report(
    df,
    converged_info,
    convergence_report,
    scenarios,
    runtime_measure,
    normalize_runtime,
):
    """Create a DataFrame with all information needed for the rank report.

    Args:
        df (pandas.DataFrame): contains 'problem', 'algorithm' and 'runtime_measure'
            as columns.
        converged_info (pandas.DataFrame): columns are the algorithms, index are the
            problems. The values are boolean and True when the algorithm arrived at
            the solution with the desired precision.
        convergence_report (pandas.DataFrame): columns are the scenarios (i.e.
            algorithms) and the dimensionality of the problems, index are the
            problems. For the scenario columns, the values are strings that are either
            "success" "failed", or "error".
        scenarios (list): list of the names of the algorithms that should be included
            in the report.
        runtime_measure (str): "n_evaluations", "n_batches" or "walltime".
            This is the runtime until the desired convergence was reached by an
            algorithm. This is called performance measure by Moré and Wild (2009).
        normalize_runtime (bool): If True the runtime each algorithm needed for each
            problem is scaled by the time the fastest algorithm needed. If True, the
            resulting plot is what Moré and Wild (2009) called data profiles.

    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms), index are the
            problems. The values are the ranks of the algorithms for each problem,
            0 means the algorithm was the fastest, 1 means it was the second fastest
            and so on. If an algorithm did not converge on a problem, the value is
            "failed".

    """
    solution_times = df.groupby(["problem", "algorithm"])[runtime_measure].max()

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
    rank_report[~converged_info] = convergence_report[scenarios]

    return rank_report


def _create_traceback_report(results, scenarios, options):
    """Create a DataFrame with the traceback of all problems that have not been solved.

    Args:
        results (dict): estimagic benchmarking results dictionary. Keys are
            tuples of the form (problem, algorithm), values are dictionaries of the
            collected information on the benchmark run, including 'criterion_history'
            and 'time_history'.
        scenarios (list): list of the names of the algorithms that should be included
            in the report.
        options (dict): dictionary with the following keys:
            - stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y".
                Determines how convergence is determined from the two precisions.
            - x_precision (float or None): how close an algorithm must have gotten to
                the true parameter values (as percent of the Euclidean distance between
                start and solution parameters) before the criterion for clipping and
                convergence is fulfilled.
            - y_precision (float or None): how close an algorithm must have gotten to
                the true criterion values (as percent of the distance between start
                and solution criterion value) before the criterion for clipping and
                convergence is fulfilled.
            - runtime_measure (str): "n_evaluations", "n_batches" or "walltime".
            - normalize_runtime (bool): If True the runtime each algorithm needed for
                each problem is scaled by the time the fastest algorithm needed. If
                True, the resulting plot is what Moré and Wild (2009) called data
                profiles.
            - include_all_tracebacks (bool): If True, all tracebacks of all scenarios
                are included in the traceback report. If False, only tracebacks of the
                tranquilo algorithms are included.
            - include_all_non_converged (bool): If True, all convergence plots of all
                algorithms that have not converged on a problem are included in the
                convergence report. If False, only problems that have not been solved
                by tranquilo are included.

    Returns:
        pandas.DataFrame: columns are the scenarios (i.e. algorithms), index are the
            problems. The values are the traceback of the algorithms for each problem
            the algorithm stopped with an error.

    """
    if options["include_all_tracebacks"]:
        traceback_scenarios = scenarios
    else:
        traceback_scenarios = [s for s in scenarios if "tranquilo" in s]

    tracebacks = {}
    for scenario in traceback_scenarios:
        tracebacks[scenario] = {}

    for key, value in results.items():
        if isinstance(value["solution"], str):
            tracebacks[key[1]][key[0]] = value["solution"]

    traceback_report = pd.DataFrame.from_dict(tracebacks, orient="columns")

    return traceback_report


def _process_report_options_and_set_defaults(options):
    """Process report options and set defaults.

    Args:
        options (dict): dictionary of the report options with the keys below.
            In case any of them are missing, we set the default values.
            - stopping_criterion (str): one of "x_and_y", "x_or_y", "x", "y".
                Determines how convergence is determined from the two precisions.
            - x_precision (float or None): how close an algorithm must have gotten to
                the true parameter values (as percent of the Euclidean distance between
                start and solution parameters) before the criterion for clipping and
                convergence is fulfilled.
            - y_precision (float or None): how close an algorithm must have gotten to
                the true criterion values (as percent of the distance between start
                and solution criterion value) before the criterion for clipping and
                convergence is fulfilled.
            - runtime_measure (str): "n_evaluations", "n_batches" or "walltime".
            - normalize_runtime (bool): If True the runtime each algorithm needed for
                each problem is scaled by the time the fastest algorithm needed. If
                True, the resulting plot is what Moré and Wild (2009) called data
                profiles.
           - include_all_tracebacks (bool): If True, all tracebacks of all scenarios
                are included in the traceback report. If False, only tracebacks of the
                tranquilo algorithms are included.
            - include_all_non_converged (bool): If True, all convergence plots of all
                algorithms that have not converged on a problem are included in the
                convergence report. If False, only problems that have not been solved
                by tranquilo are included.

    Returns:
        dict: dictionary with the keys as described above, where missing keys have been
            set to their default values.

    """
    return {
        "stopping_criterion": options.get("stopping_criterion", "y"),
        "x_precision": options.get("x_precision", None),
        "y_precision": options.get("y_precision", None),
        "runtime_measure": options.get("runtime_measure", "n_evaluations"),
        "normalize_runtime": options.get("normalize_runtime", False),
        "include_all_tracebacks": options.get("include_all_tracebacks", False),
        "include_all_non_converged": options.get("include_all_non_converged", False),
    }

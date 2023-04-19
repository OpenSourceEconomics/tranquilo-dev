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

        for plot_type in ["profile", "deviation"]:
            doc.add_heading(f"{plot_type.capitalize()} Plot", level=2)
            doc.add_paragraph(
                f"""
                ![{plot_type}](../_static/bld/figures/{plot_type}_plots/{name}.svg)
                """
            )

        converged_info = _get_convergence_info(
            info=info, path_to_results=path_to_results
        )

        doc.add_heading("Convergence Report", level=2)
        rows = converged_info.reset_index().values.tolist()
        header = ["problem"] + info["scenarios"]
        doc.add_table(header, rows)

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

    return converged_info

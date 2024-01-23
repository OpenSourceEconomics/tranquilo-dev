import shutil

import estimagic as em
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import SPHINX_STATIC_BLD


SPHINX_FIGURES = SPHINX_STATIC_BLD / "figures"
BLD_FIGURES = BLD / "figures"

for name, info in PLOT_CONFIG.items():

    for plot_type in ["profile", "deviation"]:
        source_file = BLD_FIGURES / f"{plot_type}_plots" / f"{name}.svg"
        dest_file = SPHINX_FIGURES / f"{plot_type}_plots" / f"{name}.svg"

        @pytask.mark.depends_on(source_file)
        @pytask.mark.produces(dest_file)
        @pytask.mark.task(id=f"copy_{plot_type}_plot_{name}")
        def task_copy_file(depends_on, produces):
            shutil.copyfile(depends_on, produces)

    plot_type = "convergence"
    source_files = {}
    dest_files = {}

    problems = em.get_benchmark_problems(**PROBLEM_SETS[info["problem_name"]])
    for problem in problems.keys():
        source_files[problem] = (
            BLD_FIGURES
            / f"{plot_type}_plots"  # noqa: W503
            / f"{name}"  # noqa: W503
            / f"{problem}.svg"  # noqa: W503
        )
        dest_files[problem] = (
            SPHINX_FIGURES
            / f"{plot_type}_plots"  # noqa: W503
            / f"{name}"  # noqa: W503
            / f"{problem}.svg"  # noqa: W503
        )

    @pytask.mark.depends_on(source_files)
    @pytask.mark.produces(dest_files)
    @pytask.mark.task(id=f"copy_{plot_type}_plots_{name}")
    def task_copy_files_convergence_plots(depends_on, produces):
        for key in depends_on.keys():
            shutil.copyfile(depends_on[key], produces[key])

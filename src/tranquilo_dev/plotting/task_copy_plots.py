import shutil

import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import PLOT_TYPES
from tranquilo_dev.config import SRC

PUBLIC = SRC / "slidev" / "public"

PUBLICATION_PLOTS = [name for name in PLOT_CONFIG if "publication_" in name]

for plot_type in PLOT_TYPES:

    for plot_name in PUBLICATION_PLOTS:

        _plot_name = plot_name.removeprefix("publication_")

        source_file = BLD / "bld_paper" / f"{plot_type}s" / f"{_plot_name}.svg"
        dest_file = PUBLIC / "bld_paper" / f"{plot_type}s" / f"{_plot_name}.svg"

        @pytask.mark.depends_on(source_file)
        @pytask.mark.produces(dest_file)
        @pytask.mark.task(id=f"copy_{plot_type}_plot_{plot_name}")
        def task_copy_file(depends_on, produces):
            shutil.copyfile(depends_on, produces)

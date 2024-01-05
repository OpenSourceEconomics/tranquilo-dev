import shutil

import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SRC

PUBLIC = SRC / "slidev" / "public"

for name in PLOT_CONFIG:
    for plot_type in ["profile", "convergence", "deviation"]:
        source_file = BLD / "figures" / f"{plot_type}_plots" / f"{name}.pdf"
        dest_file = PUBLIC / "bld" / "figures" / f"{plot_type}_plots" / f"{name}.pdf"

        @pytask.mark.depends_on(source_file)
        @pytask.mark.produces(dest_file)
        @pytask.mark.task(id=f"copy_{plot_type}_plot_{name}")
        def task_copy_file(depends_on, produces):
            shutil.copyfile(depends_on, produces)

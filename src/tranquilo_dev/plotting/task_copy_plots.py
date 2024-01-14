import shutil

import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import OPTIONS
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SRC
from tranquilo_dev.plotting.task_create_presentation_illustrations import (
    ILLUSTRATION_PLOT_NAMES,
)

PUBLIC = SRC / "slidev" / "public"

# ======================================================================================
# Collect all source files and their destination
# ======================================================================================
PUBLICATION_PLOTS = [name for name in PLOT_CONFIG if "publication_" in name]

SOURC_FILES = []
DEST_FILES = []

for plot_type in OPTIONS.PLOT_TYPES:
    for plot_name in PUBLICATION_PLOTS:
        _plot_name = plot_name.removeprefix("publication_")

        SOURC_FILES.append(BLD / "bld_paper" / f"{plot_type}s" / f"{_plot_name}.svg")
        DEST_FILES.append(PUBLIC / "bld_paper" / f"{plot_type}s" / f"{_plot_name}.svg")


for plot_name in ILLUSTRATION_PLOT_NAMES:
    SOURC_FILES.append(BLD / "bld_slidev" / plot_name)
    DEST_FILES.append(PUBLIC / "bld_slidev" / plot_name)


# ======================================================================================
# Copy files
# ======================================================================================
for source_file, dest_file in zip(SOURC_FILES, DEST_FILES):

    @pytask.mark.depends_on(source_file)
    @pytask.mark.produces(dest_file)
    @pytask.mark.task(id=str(source_file.relative_to(BLD)))
    def task_copy_file(depends_on, produces):
        shutil.copyfile(depends_on, produces)

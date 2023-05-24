import shutil

import pytask
from pytask_latex import compilation_steps as cs
from tranquilo_dev.config import AUX_PAPER
from tranquilo_dev.config import BLD_PAPER

OPTIONS = (
    "--pdf",
    "--interaction=nonstopmode",
    "--synctex=1",
    "--cd",
    "--quiet",
    "--shell-escape",
    "-f",
)


@pytask.mark.latex(
    script="tranquilo.tex",
    document=AUX_PAPER / "tranquilo.pdf",
    compilation_steps=cs.latexmk(options=OPTIONS),
)
def task_compile_paper():
    pass


@pytask.mark.depends_on(AUX_PAPER / "tranquilo.pdf")
@pytask.mark.produces(BLD_PAPER / "tranquilo.pdf")
@pytask.mark.task
def task_copy_paper(depends_on, produces):
    shutil.copyfile(depends_on, produces)

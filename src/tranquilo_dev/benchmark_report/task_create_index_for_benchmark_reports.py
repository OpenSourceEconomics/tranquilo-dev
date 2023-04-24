import pytask
import snakemd
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SPHINX
from tranquilo_dev.config import SPHINX_PAGES_BLD


DEPS = {}
for name in PLOT_CONFIG.keys():
    DEPS[name] = SPHINX_PAGES_BLD / f"{name}.md"


@pytask.mark.depends_on(DEPS)
@pytask.mark.produces(SPHINX / "index.md")
def task_create_index(produces):
    doc = snakemd.new_doc()

    doc.add_heading("Welcome to tranquilo-dev's benchmark reports!")
    doc.add_paragraph("This is the index page of the benchmark reports.")

    pages = "\n".join([f"bld/{name}" for name in PLOT_CONFIG.keys()])

    doc.add_raw(f"```{{toctree}} \n--- \nmaxdepth: 1 \n--- \n{pages}\n```")

    doc.add_paragraph(
        """
        {ref}`search`
        """
    )

    doc.dump(produces.parent / "index")

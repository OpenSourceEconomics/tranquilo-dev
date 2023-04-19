import pytask
import snakemd
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SPHINX
from tranquilo_dev.config import SPHINX_PAGES_BLD


@pytask.mark.depends_on(SPHINX_PAGES_BLD / f"{list(PLOT_CONFIG.keys())[0]}.md")
@pytask.mark.produces(SPHINX / "index.md")
def task_generate_index():
    doc = snakemd.new_doc()

    doc.add_heading("Welcome to tranquilo-dev's benchmark report!")

    pages = "\n".join([f"bld/{name}" for name in PLOT_CONFIG.keys()])

    doc.add_raw(f"```{{toctree}} \n--- \nmaxdepth: 1 \n--- \n{pages}\n```")

    doc.add_paragraph(
        """
        **Useful links for search:** {ref}`genindex` | {ref}`modindex` | {ref}`search`
        """
    )

    doc.dump(SPHINX / "index")

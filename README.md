# Tranquilo Development Repository

## Getting Started

Get started by installing the conda environment.

```bash
cd /path/to/project_root
conda env create -f environment.yml
conda activate tranquilo_dev
```

## Presentation

Our presentation is compiled to HTML using [marp](https://marp.app/), which needs to be
installed and made available to the PATH.

**Installation:**

- marp: Can be installed from the
  [README instructions](https://github.com/marp-team/marp-cli)

**Rendering:**

When running `pytask` marp is automatically executed with the correct flags. For the
development process it is, however, easier to run marp directly. In this case, change
into the directory where the markdown file you want to render is stored. Then run

```bash
marp --html --watch --theme-set custom.scss -- main.md
```

Now you can edit the markdown file while the rendered HTML version is continuously
updated (view it in a browser).

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[cookiecutter-pytask-project](https://github.com/pytask-dev/cookiecutter-pytask-project)
template.

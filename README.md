# Tranquilo Development Repository

*Janoś Gabler, Sebastian Gsell, Tim Mensinger, Mariam Petrosyan*

The materials in this repository can be used to reproduce all results presented in the
paper.

## Getting Started

Do you want to reproduce the results of the paper, then check out Section
[Reproducing the Results](#reproducing-the-results). If you want to work on the
development of the *tranquilo* algorithm, then check out Section
[Tranquilo Development](#tranquilo-development).

### Reproducing the Results

Get started by cloning this repository and editing the `environment.yml` file such that
the line `- -e ../tranquilo` is commented out and the line directly below is
uncommented, i.e.

```yaml
# contents of environment.yml
...

  # - -e ../tranquilo
  - git+https://github.com/OpenSourceEconomics/tranquilo

...
```

Then continue to install the conda environment.

> \[!TIP\] Check out
> [this](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
> tutorial if you are new to conda, and if you need to install conda we recommend
> installing [miniconda](https://docs.conda.io/projects/miniconda/en/latest/).

Once conda is installed, the standard practice is to open a terminal and execute

```console
$ cd /into/tranquilo-dev/folder
$ conda env create -f environment.yml
```

> \[!IMPORTANT\] If you want to execute the code in this repository in parallel, open
> the file [`src/tranquilo_dev/config.py`](./src/tranquilo_dev/config.py) and set the
> number of preferred cores when instantiating the project options like so:
>
> ```python
> OPTIONS = ProjectOptions(N_CORES_DEFAULT=8)
> ```

If the environment installation succeeded (and you've set the number of cores for the
parallel computing) open a terminal and execute:

```console
$ cd /into/tranquilo-dev/folder
$ conda activate tranquilo-dev
$ pytask
```

This will run all the requested benchmarks and plots all the figures. If the `pytask`
command executed successfully, you should be able to see a new folder called `bld` at
the root of the project. Here you find the raw benchmark results, the figures, and a
folder called `bld_paper`, where you can find all figures that are used in the paper.

#### Presentation

To reproduce the presentation, see the description
[here](./src/tranquilo_dev/slidev/README.md).

### Tranquilo Development

If you want to work on the *tranquilo* development, you have to adhere to the folder
structure below:

```
parent_folder
  - tranquilo (git clone https://github.com/OpenSourceEconomics/tranquilo.git)
  - tranquilo-dev
```

> \[!WARNING\] Do not alter the `environment.yml` file, as explained in Section
> [Reproducing the Results](#reproducing-the-results).

Open a terminal and execute

```console
$ cd /into/tranquilo-dev/folder
$ conda env create -f environment.yml
$ conda activate tranquilo_dev
```

Now you can alter the *tranquilo* codebase and are able to see the results on the
benchmarks when running

```console
$ pytask
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[cookiecutter-pytask-project](https://github.com/pytask-dev/cookiecutter-pytask-project)
template.

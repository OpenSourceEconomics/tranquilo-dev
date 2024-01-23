import matplotlib.pyplot as plt
import numpy as np
import pytask
import seaborn as sns
from tranquilo.bounds import Bounds
from tranquilo.region import Region
from tranquilo.sample_points import get_sampler
from tranquilo_dev.config import BLD


COLORS = {
    "blue": "#5778a4",
    "green": "#6a9f58",
    "orange": "#e49444",
    "red": "#d1615d",
    "teal": "#85b6b2",
    "yellow": "#e7ca60",
    "purple": "#a87c9f",
    "pink": "#f1a2a9",
    "brown": "#967662",
    "gray": "#b8b0ac",
}

PRODUCT = BLD / "bld_paper" / "illustrations" / "optimal_sphere_samples.pdf"


@pytask.mark.produces(PRODUCT)
def task_create_sphere_sample_plot(produces):
    samples = create_sphere_samples()
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    for ax, sample in zip(axes.flatten(), samples):
        plot_circle([0, 0], 1, ax)
        plot_points(sample, ax)
        style_axis(ax)
    add_labels(fig, axes)
    fig.tight_layout()
    fig.savefig(produces)


def create_sphere_samples():
    sampler_options = {
        "criterion": "distance",
        "algo_options": {"maxiter": 600, "ftol": 1e-5, "gtol": 1e-6},
        "hardness": 100,
    }

    sampler = get_sampler(sampler="optimal_hull", user_options=sampler_options)
    region = Region(center=np.array([0, 0]), radius=1)
    rng = np.random.default_rng(42)

    existing_points = [
        np.array([[0, 1]]),
        np.array([[0, 1]]),
        np.array([[0, 1]]),
        np.array([[0, 0], [0, 1]]),
        np.array([[0, 0], [0, 1]]),
        np.array([[0, 0], [0, 1]]),
    ]

    sample_sizes = [2, 3, 5, 5, 6, 8]

    samples = []
    for points, size in zip(existing_points, sample_sizes):
        new = sampler(region, n_points=size - len(points), existing_xs=points, rng=rng)
        sample = np.vstack([points, new])
        samples.append(sample)

    samples[0] = np.array([[0, 1], [0, -1]])

    return samples


def create_cube_samples():
    sampler_options = {
        # "criterion": "distance",
        # "algo_options": {"maxiter": 200},
        # "hardness": 100,
    }

    sampler = get_sampler(sampler="optimal_hull", user_options=sampler_options)
    bounds = Bounds([-1, -1], [1, 1])
    region = Region(center=np.array([0, 0]), radius=2, bounds=bounds)
    rng = np.random.default_rng(42)

    existing_points = [
        np.array([[-1, 1]]),
        np.array([[-1, 1]]),
        np.array([[-1, 1]]),
        np.array([[0, 0], [-1, 1]]),
        np.array([[0, 0], [-1, 1]]),
        np.array([[0, 0], [-1, 1]]),
    ]

    sample_sizes = [2, 3, 5, 5, 6, 8]

    samples = []
    for points, size in zip(existing_points, sample_sizes):
        new = sampler(region, n_points=size - len(points), rng=rng)
        sample = np.vstack([points, new])
        samples.append(sample)

    return samples


def plot_circle(center, radius, ax):
    ax.add_artist(plt.Circle(center, radius, color=COLORS["gray"], fill=False))
    return ax


def plot_rectangle(lb, ub, ax):
    ax.add_artist(
        plt.Rectangle(
            lb, ub[0] - lb[0], ub[1] - lb[1], color=COLORS["gray"], fill=False
        )
    )
    return ax


def plot_points(points, ax):
    ax.scatter(points[:, 0], points[:, 1], color=COLORS["blue"], s=50)
    return ax


def style_axis(ax):
    ax.set_xlim([-1.05, 1.05])
    ax.set_ylim([-1.2, 1.05])
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    sns.despine(ax=ax, left=True, bottom=True)

    return ax


def add_labels(fig, axes):
    axes[0, 0].set_ylabel("Linear ($d=3$)", fontsize=14)
    axes[1, 0].set_ylabel("Quadratic ($d=6$)", fontsize=14)
    axes[0, 0].set_xlabel("$n=2$", fontsize=14)
    axes[0, 1].set_xlabel("$n=3$", fontsize=14)
    axes[0, 2].set_xlabel("$n=5$", fontsize=14)
    axes[1, 0].set_xlabel("$n=5$", fontsize=14)
    axes[1, 1].set_xlabel("$n=6$", fontsize=14)
    axes[1, 2].set_xlabel("$n=8$", fontsize=14)
    fig.suptitle("Optimal samples on a sphere", fontsize=18)

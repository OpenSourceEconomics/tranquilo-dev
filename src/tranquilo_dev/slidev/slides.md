---
# try also 'default' to start simple
theme: default
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
# background: https://source.unsplash.com/collection/94734566/1920x1080
# apply any windi css classes to the current slide
class: 'text-center'
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# show line numbers in code blocks
lineNumbers: false
# some information about the slides, markdown enabled
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
# persist drawings in exports and build
drawings:
  persist: false
# page transition
transition: slide-left
# use UnoCSS
css: unocss
---

# Tranquilo
## A trustregion optimizer for economists by economists

Janoś Gabler, University of Bonn

Sebastian Gsell, LMU Munich

Tim Mensinger, University of Bonn

Mariam Petrosyan, University of Bonn



---
layout: center
---

# Prototypical optimization problems

<div class="grid grid-cols-2 gap-4">
<div>

## Agent-based Covid Model

- Fit simulated time series to data
- Computational bottleneck is serial
- Simulated cases are noisy
- 6 to 10 parameters
- Function evaluation takes 30 minutes
- Could only be solve with manual intervention
</div>
<div>

## DCDP Models

- Fit simulated choices to data
- Backwards induction is hard to parallelize
- Simulated choices are noisy
- 10 to 50 parameters
- Function evaluation takes between a few seconds and minutes

</div>
</div>

---
layout: center
---

# Goals

- Robust if function evaluations are noisy
- Parallelize at the level of function evaluations
- Suitable for data fitting problems
- Designed for non-expert users
- Assumption: Criterion function is expensive!
- Internally: Modular framework for algorithm development

---
layout: center
---

# Optimization Problems

<div class="grid grid-cols-2 gap-12">
<div>

## Scalar Derministic


$\text{min}_{l \leq x \leq u} F(x)$

## Scalar Noisy

$\text{min}_{l \leq x \leq u} \mathbb{E} F(x, \epsilon)$

</div>
<div>

## Least-squares Deterministic

$\text{min}_{l \leq x \leq u} F(x) = \sum_{i} f_i(x)^2$

## Least-squares Noisy

$\text{min}_{l \leq x \leq u} \mathbb{E} F(x, \epsilon) = \mathbb{E} \sum_{i} f_i(x, \epsilon_i)^2$


</div>
</div>

---
layout: center
---

# Existing optimizers

|              | Nelder-Mead| Bobyqa     | PyBobyqa   |DFO-LS       |Pounders     | Parallel NM |
|--------------|------------|------------|------------|-------------|-------------|-------------|
| Library      | Nlopt      | Nlopt      | NAG        | NAG         | TAO         | (estimagic) |
| Class        | simplex    | trustregion| trustregion| trustregion | trustregion |simplex      |
| Noisy        | 〰         | ❌         | ✅         | ✅          | ❌          |〰           |
| Parallel     | ❌         | ❌         | 〰         | 〰          | ❌          | ✅           |
| Least-squares| ❌         | ❌         | ❌         |✅          | ✅          | ❌           |

---
layout: center
---

# Steps of a derivative free trustregion optimizer

- Define a region around current x (the trustregion)
- Maintain a sample around current x on which criterion is evaluated
- Fit a regression or interpolation model on the sample
- Optimize the surrogate model to create a candidate
- Accept or reject the candidate
- Adjust the radius

---
layout: center
---

# Model quality, Rho and radius management


<div class="flex gap-8">
<div>

$F$: criterion function

$k$: iteration counter

$x_k$: current x

$s_k$: candidate step

$M_k$: surrogate model

$\rho = \frac{F(x_k) - F(x_k + s_k)}{M_k(x_k) - M_k(x_k + s_k)}$

</div>
<div>

- Goal: Sample as few new points as possible
- Model only needs to be good enough to point downhill
  - No lower bound on $R^2$ or sample geometry
- Taylor like error bounds on surrogate model
  - Small $\rho$: decrease radius
  - Large $\rho$: increase radius
- Preview: This will fail in noisy case!


</div>
</div>


---
layout: center
---

# A simple example: $f(x) = \sum_i x_i^2$

<img src="sphere.png" class="rounded" width="500" />

---
layout: center
transition: fade-out
---

<img src="animation_0.svg" class="rounded" width="600" />


---
layout: center
transition: fade-out
---

<img src="animation_1.svg" class="rounded" width="600" />


---
layout: center
transition: fade-out
---

<img src="animation_2.svg" class="rounded" width="600" />


---
layout: center
transition: fade-out
---

<img src="animation_3.svg" class="rounded" width="600" />


---
layout: center
transition: fade-out
---

<img src="animation_4.svg" class="rounded" width="600" />


---
layout: center
transition: fade-out
---

<img src="animation_5.svg" class="rounded" width="600" />



---
layout: center
---

# Exploiting least squares structure




---
layout: center
---

# Benchmark: Tranquilo vs. other optimizers

<img src="bld/figures/profile_plots/scalar_and_ls.svg" class="rounded" width="700" />


---
layout: center
---

# Cost model for parallel optimization




---
layout: center
---

# Tranquilo strategies for parallelization



---
layout: center
---

# Benchmark: Parallel tranquilo vs. DFOLS

<img src="bld/figures/profile_plots/parallelization_ls.svg" class="rounded" width="700" />


---
layout: center
---

# Problems caused by noise in trustregion optimizers


---
layout: center
---

# How DFOLS handles noise


---
layout: center
---

# Why is it so hard to pick `n_evaluations`?


---
layout: center
---

# Simulation for the sampling step



---
layout: center
---

# Power analysis for the acceptance step



---
layout: center
---

# Benchmark: Noisy tranquilo vs. DFOLS

<img src="bld/figures/profile_plots/noisy_ls.svg" class="rounded" width="700" />


---
layout: center
---

# Summary



---
layout: center
---

# Outlook

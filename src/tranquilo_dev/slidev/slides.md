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

<p style="font-size: 2.5em;text-align:left;">Tranquilo</p>
<hr>
<p style="font-size: 1.15em;text-align:left;">An Optimizer for the Method of Simulated Moments</p>

<br>

<p style="text-align:left">

Janoś Gabler*

Sebastian Gsell<sup>+</sup>

<p style="color:#04539C;font-size:1.15em;"><b>Tim Mensinger*</b></p>

Mariam Petrosyan*

</p>

<br>
<hr>
<hr>
<p style="text-align:left">
*University of Bonn <span style="float:right;">BGSE Applied Microeconomics Workshop</span><br>
<sup>+</sup>LMU Munich <span style="float:right;">January 19th 2024</span>
</p>



---
layout: center
---

# Outline


- Motivation

- Literature Review

- The Algorithm
  
  - Background

  - Noise free and serial

  - Parallel

  - Noisy


---
layout:center
---

# Motivation

<div style="display:flex;justify-content:center;align-items:center;height:500px;">
<img src="motivation/front_page.png" class="image" width="700" style="border: 2px solid black;"/>
</div>


---
layout:center
---

<div style="display:flex;justify-content:center;align-items:center;height:500px;">
<img src="motivation/outline.png" class="image" width="700" style="border: 2px solid black;"/>
</div>

---
layout:center
---

<div style="display:flex;justify-content:center;align-items:center;height:500px;">
<img src="motivation/model.png" class="image" width="700" style="border: 2px solid black;"/>
</div>

---
layout:center
---

<div style="display:flex;justify-content:center;align-items:center;height:500px;">
<img src="motivation/parameter_example.png" class="image" width="700" style="border: 2px solid black;"/>
</div>

---
layout:center
---

<div style="display:flex;justify-content:center;align-items:center;height:500px;">
<img src="motivation/estimation.png" class="image" width="700" style="border: 2px solid black;"/>
</div>



---
layout: center
---

# Prototypical problem


- Example as before: discrete choice dynamic programming model

- For each parameter $\theta$<br>1. Solve model (backwards induction)<br>2. Simulate from solved model ($\implies m(\theta)$)
- Fit simulated choices to data (make $\|m(\theta) - m^{data}\|_W$ small)
- *Problem:* Solution is slow and backwards induction is hard to parallelize<br>
  (Single evaluation of $m(\theta)$ can take a few minutes)
- *Problem:* Simulated choices are noisy<br>
  ($m(\theta, seed=12345) \neq m(\theta, seed=54321)$)
- *Constraint:* Derivative of $m(\theta)$ is not available

---
layout: center
---

# Goals for an Optimizer

- Robust to noise

- Parallel function evaluations<br>
  ($m(\theta_1)$ and $m(\theta_2)$ can be evaluated at the same time)
- Suitable for data fitting problems<br>
  (Non-linear least squares)
- Designed for non-expert users<br>
  (Adaptive option handling)
- **Key assumption:** Criterion function is expensive!<br>
  Evaluating $m(\theta)$ takes at least a few seconds

---
layout: center
---

# Optimization Problems

<div class="grid grid-cols-2 gap-12">
<div>

## Scalar Derministic


$\min_{l \leq x \leq u} f(x)$

## Scalar Noisy

$\min_{l \leq x \leq u} \mathbb{E} \left[\, f(x, \xi) \right]$

</div>
<div>

## Least-squares Deterministic

$f(x) = \sum_{i} r_i(x)^2 \to \min$

## Least-squares Noisy

$\mathbb{E} \left[\, f(x, \xi) \right] = \mathbb{E} \left[\sum_{i} r_i(x, \xi)^2 \right] \to \min$


</div>
</div>

---
layout: center
---

# What do we need for MSM Problems?

- Let $\bar{m}(\theta) = m(\theta) - m^{data}$

- MSM objective function: $g(\theta) = \bar{m}(\theta)^\top W \bar{m}(\theta)$
- Cholesky Decomposition: $W = L L^\top$
- Define $r(\theta) = L^\top \bar{m}(\theta)$
- $g(\theta) = r(\theta)^\top r(\theta) = \sum_j r_j(\theta)^2$<br>
  $\implies g$ has a least-squares structure
- And, in fact we want to erradicate simulation noise, i.e.<br>
  $g^\ast(\theta) = \mathbb{E}\left[g(\theta)\right]$

---
layout: center
---

# What about linear least squares?

- Define residual $r_i(\beta) = y_i - x_i^\top \beta$

- $\hat{\beta} = \arg\min \sum_i r_i(\beta)^2$

  Closed form solution exists! OLS!
  
- Can our optimizer find $\hat{\beta}$? *In principle, yes!*

- Should you do it? *Definitely, no!*


---
layout: center
---

# Existing Optimizers


|              | Nelder-Mead| Bobyqa     | PyBobyqa   |DFO-LS       |POUNDERS     | Parallel NM |
|--------------|------------|------------|------------|-------------|-------------|-------------|
| Class        | Simplex    | TR         | TR         | TR          | TR          | Simplex     |
| Noisy        | $\color{orange} (Yes)$      | $\color{red} No$         | $\color{green} Yes$        | $\color{green} Yes$         | $\color{red} No$          | $\color{orange} (Yes)$       |
| Parallel     | $\color{red} No$         | $\color{red} No$         | $\color{orange} (Yes)$      | $\color{orange} (Yes)$       | $\color{red} No$          | $\color{green} Yes$         |
| Least-squares| $\color{red} No$         | $\color{red} No$         | $\color{red} No$         | $\color{green} Yes$         | $\color{green} Yes$         | $\color{red} No$          |

<br>

[Nelder and Mead (1965)](), [Powell (2009)](), [Cartis et al. (2019)](), [Wild (2017)](),<br><br>
[Donghoon and Wiswall (2007)]()


---
layout: center
---

# How to Compare Optimizers

- Benchmark set [(Moré-Wild, 2019)]()

- 52 least-squares problems with 2 to 12 parameters
- Used in POUNDERS [(Wild, 2017)](), PyBobyqa and DFO-LS [(Cartis et al., 2019)]()
- Differentiable (but we don't use derivatives)
- **Visualize:** Performance profile plots
  - Y-axis: Share of solved problems
  - X-axis: Computational budget<br>
    For each problem, budget is standardized by the cost of the best optimizer


---
layout: center
---

# Why we want to utilize the least square structure

<br>
<br>
<img src="bld_slidev/profile_plots/scalar_vs_ls_benchmark_mw.svg" class="rounded" width="550" />

---
layout: fact
---

<p style="font-size: 3em;">Recap: Trust-region optimizers</p>


---
layout: center
---

# Derivative free trust-region optimization

- Start with initial parameter $x_0$

- ...
- In iteration $k$, define a region around $x_k$ given some radius
- Sample points $x$ from that region and evaluate corresponding $f(x)$
- Build a regression (or interpolation) model given $x$ and $f(x)$
- Find the minimizer of that (surrogate) model: $x_{cand}$
- Evaluate the function at the candidate: $f(x_{cand})$
- Accept or reject candidate **and** adjust radius

---
layout: center
---

# Model quality, Rho, and Radius


<div class="flex gap-20">
<div>

$f$: objective function

$k$: iteration counter

$x_k$: current x

$M_k$: surrogate model

$s_k$: candidate step


$\rho = \frac{f(x_k) - f(x_k + s_k)}{M_k(x_k) - M_k(x_k + s_k)}$

</div>
<div>

- Goal:
  - Sample few new points
  - Make large progress
- Model $M_k$ does **not** have to be great!
- Taylor like error bounds on $M_k$
  - Small $\rho$: decrease radius
  - Large $\rho$: increase radius
- Preview: This will fail in noisy case!


</div>
</div>

---
layout: center
---

# Rho

- From before:<br>
  Expected Improvement: $EI = M_k(x_k) - M_k(x_k + s_k)$<br>
  Actual Improvement: $AI = f(x_k) - f(x_k + s_k)$<br>
  $\rho = AI / EI$
  
- Say $EI$ large

  - $AI$ large $\implies$ Great! Let's try to expand search region!
  - $AI$ small $\implies$ Somethings not right! Let's zoom in and improve our model!


---
layout: center
---

# Least squares structure and the surrogate model

- No noise $\implies$ **Interpolation model**
- Model should allow for internal minima $\implies$ **Quadratic model**<br>
  How many $x$ points do we need to sample to get
  - Fully determined: $1 + p + \frac{p(p+1)}{2}$
  - With regularization: $1 + p + p$ (or less)

- Underdetermined models often defeat intuition!

- Empirical result: Least-square structure helps
  - Fully determined linear model: $r_{i}(x) = a_{i} + b_{i}^\top x$ for each residual
  - $M(x) = \sum_i r_{i}(x)^2 = a^\top a + a^\top x + x^\top B x$
  - $\implies$ Quadratic model with just $p + 1$ points
  

---
layout: fact
---

<p style="font-size: 3em;">Noise-free and serial case</p>

---
layout: center
---

# Tranquilo and Tranquilo-LS

- <span style="color: #0E4187; font-weight: bold;">T</span>rust<span style="color: #0E4187; font-weight: bold;">R</span>egion <span style="color: #0E4187; font-weight: bold;">A</span>daptive <span style="color: #0E4187; font-weight: bold;">N</span>oise robust <span style="color: #0E4187; font-weight: bold;">QU</span>adrat<span style="color: #0E4187; font-weight: bold;">I</span>c or <span style="color: #0E4187; font-weight: bold;">L</span>inear approximation <span style="color: #0E4187; font-weight: bold;">O</span>ptimizer

- Fairly standard trust-region framework
  - Sampling: Approximate Fekete points
  - Subsolvers: GQTPAR or BNTR
  - Radius management: Same as POUNDERS
- Key differences
  - History search and variable sample size
  - Switch from round to cubic trust-regions close to bounds
  - Same code for scalar and least-squares version!

---
layout: center
---

# Tranquilo-LS in action


<div class="grid grid-cols-2 gap-12">
<div>

- Criterion function: $f(x) = \sum_i x_i^2$<br>

- Start parameters: $x_0 = (1, 1)$
- Global optimum: $x^* = (0, 0)$


</div>
<div>

<img src="sphere.png" class="rounded" width="500" />

</div>
</div>


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_0.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_1.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_2.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_3.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_4.svg" class="rounded" width="500" />


---
layout: center
transition: fade
---

<img src="bld_slidev/animation_5.svg" class="rounded" width="500" />


---
layout: center
---

# Tranquilo vs. other optimizers


<br>
<br>
<img src="bld_slidev/profile_plots/scalar_vs_ls_benchmark_mw.svg" class="rounded" width="550" />


---
layout: fact
---

<p style="font-size: 3em;">Parallel Case</p>


---
layout: center
---

# Cost model for parallel optimization

- Most economists have access to:
  - 4 to 16 cores on a laptop/desktop
  - 16 to 64 cores on a server

- In practice, criterion functions are often not parallelized:
  - Lack of knowledge or time to write parallel code
  - Some problems are hard to parallelize
- Cost model with batch size $b$:
  - Want to avoid idle cores ($b \approx$ no. of cores)
  - $b$ parallel evaluations have same cost as one

---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="bld_slidev/origin_plot.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="bld_slidev/line_points_1.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="bld_slidev/line_points_2.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 1: Parallel line search

<img src="bld_slidev/line_points_3.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="bld_slidev/origin_plot.svg" class="rounded" width="400" />

---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="bld_slidev/empty_speculative_trustregion_small_scale.svg" class="rounded" width="400" />


---
layout: center
transition: fade
---

# Idea 2: Speculative sampling

<img src="bld_slidev/sampled_speculative_trustregion_small_scale.svg" class="rounded" width="400" />


---
layout: center
---

# Combining the two

- If candidate is close to trust-region border:
  - Allocate up to three function evaluations to a line search

- If "free" function evaluations are left:
  - Do speculative sampling
- If any line-search or speculative point yields improvement
  - Accept them as new candidate point $x_{cand}$


---
layout: center
---

# Line search + Speculation

<img src="bld_slidev/line_and_speculative_points.svg" class="rounded" width="400" />


---
layout: center
---

# Parallel tranquilo vs. DFO-LS

<br>
<br>
<img src="bld_slidev/profile_plots/parallel_benchmark_mw.svg" class="rounded" width="600" />


---
layout: fact
---

<p style="font-size: 3em;">Noisy case</p>


---
layout: center
---

# Reminder and Problems

- Can compute: $f(x, \xi_1) \neq f(x, \xi_2), \dots$<br>

  think different seed, different value

- Want to evaluate: $\mathbb{E}[f(x, \xi)]$

- Model $M_k$ does not approximate $\mathbb{E}f$ well $\implies \rho$ is low in many iterations<br>
  $\implies$ Radius shrinks to zero $\implies$ Optimization fails
  
- How to get rid of noise?<br>

  Averaging: $\mathbb{E}[f(x, \xi)] \approx \frac{1}{n} \sum_{i=1}^n f(x, \xi_i)$<br>

  But, how do we choose $n$?


---
layout: center
---

# How DFO-LS handles noise


1. Evaluate criterion multiple times at each point and average<br>
   - How many evaluations is decided by the user<br>
   - Very hard to get right!

2. Re-start if trust-region collapses


---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?
<div class="grid grid-cols-2 gap-12">
<div>


<img src="bld_slidev/noise_plot_1.svg" class="rounded" width="450" />

</div>
<div>

- Goal: Find optimum of criterion ($\mathbb{E}[f(x)]$)

- Problem: Only have access to noisy evaluations $f(x)$


</div>
</div>


---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?

<div class="grid grid-cols-2 gap-12">
<div>


<img src="bld_slidev/noise_plot_2.svg" class="rounded" width="450" />

</div>
<div>

- Building surrogate model inside trust-region

- Slope dominates noise
  
- Model may be a bad approximation of $\mathbb{E}[f(x)]$, but it still sends us in the right direction<br>
  
  $\implies$ We don't care about the noise

</div>
</div>


---
layout: center
transition: fade
---

# Why is it hard to pick sample sizes?

<div class="grid grid-cols-2 gap-12">
<div>

<img src="bld_slidev/noise_plot_3.svg" class="rounded" width="450" />

</div>
<div>

- Noise dominates slope

- We need to evaluate $f$ more often on each point $x$ to average out the noise


</div>
</div>


---
layout: center
---

# [Central idea](): A different look on radius and $\rho$

<div class="grid grid-cols-2 gap-6">
<div>

## Noise-free case

- Problem: Approximation error

- Tuning parameter: Radius
- Performance metric: $\rho$
- Large approx. error $\implies$ low $\rho$ $\implies$ decrease radius $\implies$ improveme approx. error


</div>
<div>

## Noisy case

- Problem: Random error

- Tuning parameter: Sample size
- Need: $\color{#04539C} \rho_{noise}$
- Large random error $\implies$ low $\color{#04539C}\rho_{noise}$ $\implies$ increase sample size $\implies$ improve random error

</div>
</div>


---
layout: center
---

# [Central idea](): Simulate $\rho_{noise}$

- Classical $\rho = \frac{f(x_k) - f(x_k + s_k)}{M_k(x_k) - M_k(x_k + s_k)}$

  Quotient contains error due to approximation and randomness
  
- Want: $\rho_{noise}$ to only capture the error due to randomness

  We somehow need to get rid of the approximation error
  
- Idea: Compare models of same class

  $\rho_{noise} = \frac{M_k(x_k) - M_k(x_k + s_k)}{\text{Quadratic Model}}$

---
layout: center
---

# [Central idea](): Simulate $\rho_{noise}$

<br>
<br>

- $\rho_{noise} = \frac{M_k(x_k) - M_k(x_k + s_k)}{\text{Quadratic Model}}$

- Want: Difference in $M_k$ and Quadratic Model due to random error

- Given locally constant noise variance estimate $\sigma_k$:<br>
  Simulate new points $(x, M_k(x) + \sigma_k)$<br>
  ($\sigma_k$ does not require extra evaluations)

- Build new model $\tilde{M}_k$ using these points

- $\rho_{noise} = \frac{M(x_k) - M(x_k + \tilde{s}_k)}{\tilde{M_k}(x_k) - \tilde{M_k}(x_k + \tilde{s}_k)}$

- Repeat this simulation exercise many times!<br>
  $\implies$ Increase sample size if most $\rho_{noise}$'s are small


---
layout: center
---

# Noise in the acceptance step

- Noise-free acceptance step:<br>$f(x_{current}) > f(x_{cand}) \implies$ accept
  
- Noisy acceptance problem:<br>$\mathbb{E}[f(x_{current})] > \mathbb{E}[f(x_{cand})]$?
  
- $\Delta^\ast = \mathbb{E}[f(x_{current})] - \mathbb{E}[f(x_{cand})]$

- Intuition: if $\Delta^\ast$ small, we require many samples
  
- Problem is similar to effect size methodology / power analysis


---
layout: center
---

# [Central idea](): Power analysis

<br>

- Minimal detectable effect size: Use expected improvement!<br>
  $\Delta_{min} = M_k(x_{current}) - M_k(x_{cand})$
  
- Choose how many evaluations of $f$ to perform at $x_{current}$ and $x_{cand}$

- Power analysis: $\frac{n_1 n_2}{n_1 + n_2} \geq \sigma^2 \Big[\frac{\Phi^{-1}(1 - \alpha) + \Phi^{-1}(1 - \beta)}{\Delta_{min}} \Big]^2$<br>

  - $n_1, n_2$: number of evaluations at $x_{current}$ and $x_{cand}$<br>
  - $\alpha$: confidence level<br>
  - $1 - \beta$: power level<br>
  - $\sigma^2$ variance estimate
  
- Accept $x_{cand}$ if $\frac{1}{n_1} \sum_{i = 1}^{n_1} f(x_{current}, \xi_i) > \frac{1}{n_2} \sum_{i = 1}^{n_2} f(x_{cand}, \xi_i)$




---
layout: center
---

# Noisy tranquilo vs. DFO-LS

<br>
<br>
<img src="bld_slidev/profile_plots/noisy_benchmark_mw_noisy.svg" class="rounded" width="550" />


---
layout: center
---

# Summary

- We designed an algorithm for derivative-free trust-region optimization

- Performance in noise-free and serial setting is similar to existing optimizers
- Two ideas for parallelization:
  - Line search
  - Speculative sampling
- Two ideas for noise handling:
  - Simulate $\rho_{noise}$ in sampling step
  - Power analysis for acceptance step

---
layout: center
---

# Next Steps

1. Improved algorithm comparison for our case study (motivation)

1. Consider larger benchmarks (e.g., [Cartis and Roberts, 2019]())

1. Perform replication of published MSM estimations

1. Combine noisy and parallel

1. More fine tuning and working on robustness
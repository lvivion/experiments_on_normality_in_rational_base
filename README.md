# Numerical Experiments for "A normality conjecture on rational base number systems"

This repository contains the code and data to reproduce the numerical experiments from the mathematical paper:

Andrieu, Eliahou, and Vivion, A Normality Conjecture on Rational Base Number Systems, 2025.

---

## Repository structure

- `Source_code/`: python scripts to generate data and produce figures;
- `Experiments_from_the_authors/`: Generated datasets used in the paper.

---

## Source_code

- `Functions.py`: contains the functions to generate random words, generate random minimal words, compute the richness thresholds and the deviations from uniformity.
- `main.py`: runs a complete experiment for chosen parameters. Produces complete tables and sets of figures.

## Experiments_from_the_authors

- `Tables_exp1/`: Tables for the richness threshold and the deviation from uniformity for all the minimal words of the first family of experiments.
- `Tables_exp2/`: Tables for the richness threshold and the deviation from uniformity for all the minimal words of the second family of experiments. The corresponding minimal words have been computed from the random seeds, which are listed in the Seeds_basep_q.txt files.
- `Source_data_exp3/`: Tables of the randomly choosen seeds generated for the third family of experiments.
- `Figures_exp3/`: Figures of richness thresholds and deviation from uniformity for the third family of experiments.



---

- Several scripts require the external libraries NumPy and Matplotlib, which are not included in Python’s standard library. 


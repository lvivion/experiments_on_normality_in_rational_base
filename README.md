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

- `Tables_exp1/`: Experiment 1 of the paper. Tables for the richness thresholds and the deviations from uniformity of all  minimal words with valuation-seed 1 and length 10**6, for every pair of coprime integers p and q such that 1 < q < p < 10.
- `Tables_exp2/`: Experiment 2 of the paper. Tables for the richness thresholds and the deviations from uniformity for 20 randomly chosen minimal words of length 10**6 in bases 3/2, 7/2, 8/3, 8/5, 11/3, and 26/6. The list of random seeds is provided.
- `Source_data_exp3/`: Tables of the 5x10000 randomly chosen seeds generated for Experiment 3.
- `Figures_exp3/`: Experiment 3. Figures of the richness thresholds and the deviations from uniformity for 10000 randomly chosen minimal words of length 10**5 in bases 3/2, 7/2, 5/3, 11/3, 6/5.



---

- Several scripts require the external libraries NumPy and Matplotlib, which are not included in Python’s standard library. 


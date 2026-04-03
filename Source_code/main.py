#############################################################
#      author: Léo Vivion
#      last update : 04/01/2026
#
#      MAIN CODE for "A Normality Conjecture in Rational Base Number System"
#      by M. Andrieu, S. Eliahou, L. Vivion, 2026
#
#      together with Functions.py
#
#
##############################################################



import Functions as fn
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# ------------------------------------------------------------------------------------
#   General parameters 
# ------------------------------------------------------------------------------------


#   Rk: For the values of the parameters suggested here, expect approx. 5min of computation on a standard laptop.


p = 6
q = 5
seed_bound = 10 ** 6

sample_size = 10**3    # number of generated minimal and random words
N = 10**5    # length of the computed words

Lmax = 6    # largest length for which the richness threshold is computed
cut_view1 = 3    # length of the factors for which the histogram of the richness threshold is displayed. cut_view1 must be smaller than Lmax
num_intervals = 30    # number of subintervals for the histogram


length = 3    # length of the factors for which the deviation from uniformity is computed
step = 1000    # 
cut_view2 = 10**5  # length of the prefix for which the histogram of the deviation from uniformity is displayed


# ------------------------------------------------------------------------------------
# Computation of the random and minimal words
# ------------------------------------------------------------------------------------


# Rk: The computation of minimal word is the slowest function of the whole program, due to the manipulation of large integers. The largest the ratio p/q is, the slowest the function is.

os.makedirs("save", exist_ok=True)

print(f"Generating {sample_size} {q}-ary random words of length {N}")
print("Computation time =")
start = time.time()
fn.generate_random_words(q, N, sample_size)
end = time.time()
print(f"{end - start} sec")

print(f"Generating the length-{N} prefix of {sample_size} randomly chosen minimal words in base {p}/{q}")
print("Computation time =")
start = time.time()
fn.generate_random_minimal_words(p, q, N, sample_size, seed_bound)
end = time.time()
print(f"{end - start} sec")


# ------------------------------------------------------------------------------------
# Computation of the richness thresholds of the random and minimal words generated above
# ------------------------------------------------------------------------------------

print(f"Computing the richness threshold up to length {Lmax} of the {sample_size} random words")
print("Computation time =")
start = time.time()
path = os.path.join("save", "random_words.txt")
with open(path, "r") as f:
    fn.compute_richness_thresholds_list(f, q, Lmax, output_filename="richness_thresholds_rw")
end = time.time()
print(f"{end - start} sec")

print(f"Computing the richness threshold up to length {Lmax} of the {sample_size} minimal words")
print("Computation time =")
start = time.time()
path = os.path.join("save", "minimal_words.txt")
with open(path, "r") as f:
    fn.compute_richness_thresholds_list(f, q, Lmax, output_filename="richness_thresholds_mw")
end = time.time()
print(f"{end - start} sec")


# ------------------------------------------------------------------------------------
# Computation of the deviation from uniformity of the random and minimal words generated above
# ------------------------------------------------------------------------------------

print(f"Computing the length-{length} deviation from uniformity of the {sample_size} random words")
print("Computation time =")
start = time.time()
path = os.path.join("save", "random_words.txt")
with open(path, "r") as f:
    fn.compute_deviation_from_uniformity_list(f, q, length, step, output_filename="deviation_from_uniformity_rw")
end = time.time()
print(f"{end - start} sec")

print(f"Computing the length-{length} deviation from uniformity of the {sample_size} minimal words")
print("Computation time =")
start = time.time()
path = os.path.join("save", "minimal_words.txt")
with open(path, "r") as f:
    fn.compute_deviation_from_uniformity_list(f, q, length, step, output_filename="deviation_from_uniformity_mw")
end = time.time()
print(f"{end - start} sec")


# ------------------------------------------------------------------------------------
# Drawing figures for the richness threshold
# ------------------------------------------------------------------------------------

# Load data
path_RT_rw = os.path.join("save", "richness_thresholds_rw.txt")
RT_rw = np.loadtxt(path_RT_rw, delimiter=',')[:sample_size, :Lmax]

path_RT_mw = os.path.join("save", "richness_thresholds_mw.txt")
RT_mw = np.loadtxt(path_RT_mw, delimiter=',')[:sample_size, :Lmax]

# Computation of the statistics (minimum, maximum, 10th, 25th, 50th, 75th, and 90th centile
min_rw = np.min(RT_rw, axis=0)
max_rw = np.max(RT_rw, axis=0)
RT_sort = np.sort(RT_rw, axis=0)
p10_rw = RT_sort[int(0.1 * sample_size), :]
p25_rw = RT_sort[int(0.25 * sample_size), :]
p50_rw = RT_sort[int(0.50 * sample_size), :]
p75_rw = RT_sort[int(0.75 * sample_size), :]
p90_rw = RT_sort[int(0.9 * sample_size), :]

min_mw = np.min(RT_mw, axis=0)
max_mw = np.max(RT_mw, axis=0)
RT_sort = np.sort(RT_mw, axis=0)
p10_mw = RT_sort[int(0.1 * sample_size), :]
p25_mw = RT_sort[int(0.25 * sample_size), :]
p50_mw = RT_sort[int(0.50 * sample_size), :]
p75_mw = RT_sort[int(0.75 * sample_size), :]
p90_mw = RT_sort[int(0.9 * sample_size), :]


# General settings for the figures
plt.rcParams.update({
    "font.size": 16,
    "axes.linewidth": 2,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "lines.linewidth": 2,
    "mathtext.fontset": "stix",
    "font.family": "STIXGeneral",
})


# Figure 1: Comparision between the statistics of the richness threshold of minimal and random words
fig, ax = plt.subplots(figsize=(14, 12))
x = np.arange(1, Lmax + 1)

ax.plot(x, np.log(min_rw), color="lightsalmon", linewidth=2, label=rf"Random ${{{q}}}$-ary words (minimum, 10th, 25th, 50th, 75th, and 90th centile, and maximum richness thresholds)")
ax.plot(x, np.log(max_rw), color="lightsalmon", linewidth=2)
ax.plot(x, np.log(p10_rw), color="lightsalmon", linewidth=2)
ax.plot(x, np.log(p25_rw), color="lightsalmon", linewidth=2)
ax.plot(x, np.log(p50_rw), color="lightsalmon", linewidth=2)
ax.plot(x, np.log(p75_rw), color="lightsalmon", linewidth=2)
ax.plot(x, np.log(p90_rw), color="lightsalmon", linewidth=2)

ax.plot(x, np.log(min_mw), color="black", linewidth=0.7, label=rf"Minimal words in base ${{{p}/{q}}}$ (minimum, 10th, 25th, 50th, 75th, and 90th centile, and maximum richness thresholds)")
ax.plot(x, np.log(max_mw), color="black", linewidth=0.7)
ax.plot(x, np.log(p10_mw), color="black", linewidth=0.7)
ax.plot(x, np.log(p25_mw), color="black", linewidth=0.7)
ax.plot(x, np.log(p50_mw), color="black", linewidth=0.7)
ax.plot(x, np.log(p75_mw), color="black", linewidth=0.7)
ax.plot(x, np.log(p90_mw), color="black", linewidth=0.7)

ax.set_xlabel(r"$l$", fontsize=25)
ax.set_ylabel(rf"$\log(\mathrm{{rt}}_{{\mathrm{{wmin}}_{{{p}/{q}}}(u)}}(l))$", fontsize=25)
ax.set_xlim(0, Lmax+1)
ax.set_ylim(0, np.log(np.max(RT_mw))+1)
ax.legend()
fig.suptitle(rf"Comparison of the richness thresholds for {sample_size} minimal words in base {p}/{q} and {sample_size} random {q}-ary words")
for spine in ax.spines.values():
    spine.set_linewidth(2)
plt.tight_layout()

output_path = os.path.join("save", f"RT_base{p}_{q}statistics.png")
plt.savefig(output_path, dpi=300)

plt.show()

# Figure 2: A cut view
rw = RT_rw[:, cut_view1-1]
mw = RT_mw[:, cut_view1-1]

bin_min = min(rw.min(), mw.min())
bin_max = max(rw.max(), mw.max())
bins = np.linspace(bin_min, bin_max, num_intervals + 1)
        
fig, ax = plt.subplots(figsize=(14, 12))

ax.hist(rw, bins=bins, alpha=0.3, facecolor='lightsalmon', label=rf"Random ${q}$-ary words")
ax.hist(mw, bins=bins, histtype='step', color="black", linewidth=1, label=rf"Minimal words in base ${p}/{q}$")
        
ax.set_xlabel(rf"$\mathrm{{rt}}_{{w}}({cut_view1})$", fontsize=25)
ax.legend()
fig.suptitle(rf"Comparision of the distribution of $\mathrm{{rt}}_{{w}}({cut_view1})$, for {sample_size} minimal words in base {p}/{q} and {sample_size} random {q}-ary words")
for spine in ax.spines.values():
    spine.set_linewidth(2)
plt.tight_layout()

output_path = os.path.join("save", f"RT_base{p}_{q}histogram{cut_view2}.png")
plt.savefig(output_path, dpi=300)

plt.show()


# ------------------------------------------------------------------------------------
# Drawing figures for the deviation from uniformity
# ------------------------------------------------------------------------------------

# Load data
path_DfU_rw = os.path.join("save", "deviation_from_uniformity_rw.txt")
DfU_rw = np.loadtxt(path_DfU_rw, delimiter=',')[:sample_size, : (N - length +1) // step]

path_DfU_mw = os.path.join("save", "deviation_from_uniformity_mw.txt")
DfU_mw = np.loadtxt(path_DfU_mw, delimiter=',')[:sample_size, : (N - length +1) //step]

# Computation of the statistics (minimum, maximum, 10th, 25th, 50th, 75th, and 90th centile
min_rw = np.min(DfU_rw, axis=0)
max_rw = np.max(DfU_rw, axis=0)
DfU_sort = np.sort(DfU_rw, axis=0)
p10_rw = DfU_sort[int(0.1 * sample_size), :]
p25_rw = DfU_sort[int(0.25 * sample_size), :]
p50_rw = DfU_sort[int(0.5 * sample_size), :]
p75_rw = DfU_sort[int(0.75 * sample_size), :]
p90_rw = DfU_sort[int(0.9 * sample_size), :]

min_mw = np.min(DfU_mw, axis=0)
max_mw = np.max(DfU_mw, axis=0)
DfU_sort = np.sort(DfU_mw, axis=0)
p10_mw = DfU_sort[int(0.1 * sample_size), :]
p25_mw = DfU_sort[int(0.25 * sample_size), :]
p50_mw = DfU_sort[int(0.5 * sample_size), :]
p75_mw = DfU_sort[int(0.75 * sample_size), :]
p90_mw = DfU_sort[int(0.9 * sample_size), :]

# General settings for the figures
plt.rcParams.update({
    "font.size": 16,
    "axes.linewidth": 2,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "lines.linewidth": 2,
    "mathtext.fontset": "stix",
    "font.family": "STIXGeneral",
})


# Figure 1: Comparision between the statistics of the deviation from uniformity of minimal and random words
fig, ax=plt.subplots(figsize=(14, 12))
x=np.arange(length + step, N + 1, step)

ax.plot(np.log(x), np.log(min_rw), color="lightsalmon", linewidth=2, label=rf"Random ${{{q}}}$-ary words (minimum, 10th, 25th, 50th, 75th, and 90th centile, and maximum deviation from uniformity)")
ax.plot(np.log(x), np.log(max_rw), color="lightsalmon", linewidth=2)
ax.plot(np.log(x), np.log(p10_rw), color="lightsalmon", linewidth=2)
ax.plot(np.log(x), np.log(p25_rw), color="lightsalmon", linewidth=2)
ax.plot(np.log(x), np.log(p50_rw), color="lightsalmon", linewidth=2)
ax.plot(np.log(x), np.log(p75_rw), color="lightsalmon", linewidth=2)
ax.plot(np.log(x), np.log(p90_rw), color="lightsalmon", linewidth=2)

ax.plot(np.log(x), np.log(min_mw), color="black", linewidth=0.7, label=rf"Minimal words in base ${{{p}/{q}}}$ (minimum, 10th, 25th, 50th, 75th, and 90th centile, and maximum deviation from uniformity)")
ax.plot(np.log(x), np.log(max_mw), color="black", linewidth=0.7)
ax.plot(np.log(x), np.log(p10_mw), color="black", linewidth=0.7)
ax.plot(np.log(x), np.log(p25_mw), color="black", linewidth=0.7)
ax.plot(np.log(x), np.log(p50_mw), color="black", linewidth=0.7)
ax.plot(np.log(x), np.log(p75_mw), color="black", linewidth=0.7)
ax.plot(np.log(x), np.log(p90_mw), color="black", linewidth=0.7)

ax.set_xlabel(r"$\log(n)$", fontsize=25)
ax.set_ylabel(rf"$\log(D_{{\mathrm{{wmin}}_{{{p}/{q}}}(u),{{{length}}}}}(n))$", fontsize=25)
ax.legend()
fig.suptitle(rf"Comparison of the deviation from uniformity for {sample_size} minimal words in base {p}/{q} and {sample_size} random {q}-ary words")
for spine in ax.spines.values():
    spine.set_linewidth(2)
plt.tight_layout()

output_path = os.path.join("save", f"DfU_base{p}_{q}_length_{length}statistics.png")
plt.savefig(output_path, dpi=300)

plt.show()

# Figure 2: A cut view
count_rw = Counter(DfU_rw[:, (cut_view2 - length) // step - 1])
count_mw = Counter(DfU_mw[:, (cut_view2 - length) // step - 1])

fig, ax = plt.subplots(figsize=(15, 12))
ax.plot(count_rw.keys(), count_rw.values(), color="lightsalmon", linestyle="none", marker="+", markersize=8, markeredgewidth=2.5, label=rf"Random ${q}$-ary words")
ax.plot(count_mw.keys(), count_mw.values(), color="black", linestyle="none", marker="o", markersize=4, label=rf"Minimal words in base ${p}/{q}$")
    
ax.set_xlabel(rf"$D_{{w, {length}}}({cut_view2})$", fontsize=25)
ax.legend()
fig.suptitle(rf"Comparision of the distribution of the signed version of $D_{{w, {length}}}({cut_view2})$, for {sample_size} minimal words in base {p}/{q} and {sample_size} random {q}-ary words")
for spine in ax.spines.values():
    spine.set_linewidth(2)
plt.tight_layout()

output_path = os.path.join("save", f"DfU_base{p}_{q}_length_{length}histogram{cut_view2}.png")
plt.savefig(output_path, dpi=300)

plt.show()


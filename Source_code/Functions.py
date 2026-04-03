#############################################################
#      author: Léo Vivion
#      last update : 04/01/2026
#
#      Functions file for "A Normality Conjecture in Rational Base Number System"
#      by M. Andrieu, S. Eliahou, L. Vivion, 2026
#
#      together with main.py
#
#
##############################################################


import os
from itertools import product
import random

# ------------------------------------------------------------------------------------
#  Generating random words of given length using digits in {0, ..., q-1},   and saving them to a .txt file.
# ------------------------------------------------------------------------------------
def generate_random_words(q, length, sample_size, output_filename="random_words", output_dir="save"):
    """
    Generates random words of given length using digits in {0, ..., q-1},
    and saves them to a file.

    Args:
        q (int): size of the alphabet (digits from 0 to q-1)
        length (int): length of each word
        sample_size (int): number of words to generate
        output_filename (str): name of the output file (without extension), by default: "random_words"
        output_dir (str): directory where the file is saved, by default: "save"
    """
    output_path = os.path.join(output_dir, f"{output_filename}.txt")
    with open(output_path, "w") as f:
        for _ in range(sample_size):
            word = "".join(str(random.randrange(q)) for _ in range(length))
            f.write(word + "\n")


# ------------------------------------------------------------------------------------
#   computing a long prefix of the minimal word w_min_{p/q}(seed).
# ------------------------------------------------------------------------------------
def compute_minimal_word(p, q, seed, length):
    """
    
    Computes a prefix of the minimal word w_min_{p/q}(seed).
    
    Based on Remark~3.3 of the article "A normality conjecture on rational base number systems" by Andrieu, Eliahou, Vivion 2025:
        a_i = (-p * n_i) mod q
        n_{i+1} = (p * n_i + a_i) / q
    ...which is accelerated by doing a unique Euclidean division.

    Args:
        p, q (int): parameters of the base
        seed (int): seed of the minimal word
        length (int): number of digits to generate

    Returns:
        str: concatenation of generated digits
    """
    nmin = seed
    digits = list()

    for _ in range(length):
        loc, a = divmod(-p * nmin, q)    # a is the (i+1)-th letter of wmin(seed)
        nmin = -loc
        digits.append(str(a))

    return "".join(digits)


# ------------------------------------------------------------------------------------
#     Generating random seeds and computing their associated minimal words. 
# ------------------------------------------------------------------------------------
def generate_random_minimal_words(p, q, length, sample_size, seed_bound, seeds_filename="random_seeds", words_filename="minimal_words", output_dir="save"):
    """
    Generates random seeds and computes their associated minimal words. Saves them to a .txt files.

    Args:
        p, q (int): parameters of the base
        length (int): length of each generated word
        sample_size (int): number of samples to generate
        seed_bound (int): upper bound for random seeds
        seeds_filename (str): file name for seeds (without extension), by default: "random_seeds"
        words_filename (str): file name for words (without extension), by default: "minimal_words"
        output_dir (str): directory where files are saved, by default: "save"
    """

    # Generate seeds
    seeds = [random.randint(1, seed_bound) for _ in range(sample_size)]

    # Write seeds
    seeds_path = os.path.join(output_dir, f"{seeds_filename}.txt")
    with open(seeds_path, "w") as f:
        f.write("\n".join(map(str, seeds)))

    # Generate and write words
    words_path = os.path.join(output_dir, f"{words_filename}.txt")
    with open(words_path, "w") as f:
        for seed in seeds:
            word = compute_minimal_word(p, q, seed, length)
            f.write(word + "\n")


# ------------------------------------------------------------------------------------
#      Computing the richness thresholds of a word.
# ------------------------------------------------------------------------------------
def compute_richness_threshold(word, q, max_length):
    """
    Computes the richness thresholds of a word.

    For each length l (from 1 to max_length), we read the word and count
    distinct substrings of length l until reaching q**l or exhausting the word.

    Args:
        word (str): input word
        q (int): base parameter
        max_length (int): maximum substring length

    Returns:
        list[int]: results for each length l
    """
    n = len(word)
    results = list()

    for length in range(1, max_length + 1):
        target = q ** length
        seen_factors = set()
        count = 0

        for i in range(n - length + 1):
            factor = word[i:i + length]

            if factor not in seen_factors:
                seen_factors.add(factor)
                count += 1

            if count == target:
                results.append(i + length)
                break
        else:
            results.append(count - target)

    return results


# ------------------------------------------------------------------------------------
#  Computing the richness thresholds (of each word in a .txt file.)
# ------------------------------------------------------------------------------------
def compute_richness_thresholds_list(file, q, max_length, output_filename="richness_thresholds", output_dir="save"):
    """
    Computes the richness thresholds of each word in a .txt file,
    and saves the results in another .txt file.

    Args:
        file (Iterable[str]): input file (each line is a word)
        q (int): base parameter
        max_length (int): maximum substring length
        output_filename (str): name of output file (without extension), by default: "richness_thresholds"
        output_dir (str): directory to save the file, by default: "save"
    """
    output_path = os.path.join(output_dir, f"{output_filename}.txt")
    with open(output_path, "w") as f:
        for line in file:
            word = line.strip()
            thresholds = compute_richness_threshold(word, q, max_length)
            f.write(",".join(map(str, thresholds)) + "\n")


# ------------------------------------------------------------------------------------
#  Short auxiliary function
# ------------------------------------------------------------------------------------
def list_all_q_ary_words(q, length):
    """
    Generates all words of length `length` over the alphabet {0, ..., q-1}.

    Returns:
        set[str]: set of all possible words
    """
    alphabet = [str(i) for i in range(q)]
    return {"".join(p) for p in product(alphabet, repeat=length)}


# ------------------------------------------------------------------------------------
# Computing the deviation from uniformity of longer and longer prefixes of a word.
# ------------------------------------------------------------------------------------
def compute_deviation_from_uniformity(word, q, factors, length, step=1):
    """
    Computes the deviation from uniformity of longer and longer prefixes of a word.

    Args:
        word (str): input word
        q (int): alphabet size
        factors (set[str]): all possible factors of given length
        length (int): factor length
        step (int): The deviation is computed for very prefixes of length in range(length + step - 1, len(word) + 1, step)  (by default: step = 1). 
Using a larger step can speed up the computation and smooth the results.

    Returns:
        list[float]: deviation values
    """
    counts = {factor: 0 for factor in factors}
    results = list()
    n = len(word)
    target = 1 / (q ** length)
    
    cpt = 0
    for i in range(n - length + 1):
        cpt += 1
        factor = word[i:i + length]
        counts[factor] += 1
        if cpt == step:
            cpt = 0
            deviation = max(abs(counts[f] / (i + 1) - target) for f in counts)
            results.append(deviation)
    
    return results


# ------------------------------------------------------------------------------------
# Computing the deviation from uniformity for each word in a .txt file
# ------------------------------------------------------------------------------------
def compute_deviation_from_uniformity_list(file, q, length, step=1, output_filename="deviation_from_uniformity", output_dir="save"):
    """
    Computes deviation from uniformity for each word in a .txt file. Produces a .txt file.
    
    Args:
        file (Iterable[str]): input file (each line is a word)
        q (int): size of the alphabet
        length (int): factor length
        step (int): The deviation is computed every `step` values (default: step = 1). 
Using a larger step can speed up the computation and smooth the results.
        output_filename (str): name of output file (without extension), by default: "deviation_from_uniformity"
        output_dir (str): directory to save the file, by default: "save"
    """
    factors = list_all_q_ary_words(q, length)
    output_path = os.path.join(output_dir, f"{output_filename}.txt")

    with open(output_path, "w") as f:
        for line in file:
            word = line.strip()
            deviation = compute_deviation_from_uniformity(word, q, factors, length, step)
            f.write(",".join(map(str, deviation)) + "\n")


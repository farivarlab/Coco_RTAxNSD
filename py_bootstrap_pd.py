import numpy as np
import os
import matplotlib.pyplot as plt
import pydory as dory
from persim import plot_diagrams
import csv

# -------- SETTINGS --------
rdm_dir = "data"
output_dir = "tda_results"
os.makedirs(output_dir, exist_ok=True)

roi = "V1"  # Example ROI; change or loop over ROIs as needed
file_path = os.path.join(rdm_dir, f"{roi}_RDM.npy")

# -------- FUNCTIONS --------
def enclosing_radius(rdm):
    """
    Compute enclosing radius cutoff for thresholding RDM.
    Here: min of the max distances per point.
    """
    max_dists = np.max(rdm, axis=1)
    radius = np.min(max_dists)
    return radius


def threshold_rdm_to_edge_list(rdm, cutoff, output_dir, chunk_size=1000):
    """
    Convert a large RDM to an edge list CSV (distance ≤ cutoff) in a memory-safe way.
    """
    n = rdm.shape[0]
    edge_list_path = os.path.join(output_dir, f"{roi}_edge_list.csv")

    with open(edge_list_path, "w", newline='') as f:
        writer = csv.writer(f)
        for i_start in range(0, n, chunk_size):
            i_end = min(i_start + chunk_size, n)
            block = rdm[i_start:i_end]
            for i_local, row in enumerate(block):
                i = i_start + i_local
                for j in range(i + 1, n):  # Only upper triangle
                    val = row[j]
                    if val <= cutoff:
                        writer.writerow([i, j, val])

    print(f"Edge list written to {edge_list_path}")
    return edge_list_path


def run_tda(edge_lista_path, roi, output_dir, cutoff, maxdim=1):
    """
    Run PyDory on a thresholded RDM and return the persistence diagrams.
    """
    import time

    # Create output paths
    output_prefix = os.path.join(output_dir, f"{roi}_Dory")


    # Set parameters
    source = edge_lista_path
    lower_thresh = 0
    thresh = cutoff
    filetype = 2  # distance matrix
    threads = 1
    target = output_prefix
    dim = maxdim
    compute_cycles = 0
    reduce_cyc_lengths = 0
    cyc_thresh = thresh
    suppress_output = 1
    hom_batch_size = 500
    cohom_batch_size = 50

    print(f"Running PyDory on {roi}...")
    start = time.time()

    # PyDory requires all args in order (positional)
    dory.compute_PH(
        source,
        lower_thresh,
        thresh,
        filetype,
        threads,
        target,
        dim,
        compute_cycles,
        reduce_cyc_lengths,
        cyc_thresh,
        suppress_output,
        hom_batch_size,
        cohom_batch_size
    )

    print(f"PyDory completed for {roi} in {time.time() - start:.2f} seconds")

    # Read H1 persistence diagram from PyDory output
    h1_file = f"{output_prefix}H1_pers_data.txt"
    if not os.path.exists(h1_file):
        raise FileNotFoundError(f"{h1_file} not found. PyDory may have failed.")

    h1 = np.loadtxt(h1_file)
    if h1.ndim == 1:
        h1 = h1[None, :]
    return [np.array([]), h1]  # Returning only H1, H0 is placeholder



def plot_save_diagrams(diagrams, roi, output_dir):
    """
    Plot persistence diagrams and save to file.
    """
    plt.figure(figsize=(8, 6))
    plot_diagrams(diagrams, show=False)
    plt.title(f"Persistence Diagram for {roi}")
    plt.savefig(os.path.join(output_dir, f"{roi}_persistence_diagram.png"))
    plt.close()

# -------- MAIN --------
print(f"Loading {roi} RDM...")
rdm = np.load(file_path, mmap_mode='r')

print("Computing enclosing radius...")
cutoff = enclosing_radius(rdm) * 0.7
print(f"Enclosing radius cutoff: {cutoff}")

print("Thresholding RDM...")
edge_list_path = threshold_rdm_to_edge_list(rdm, cutoff, output_dir)

print("Running persistent homology...")
diagrams = run_tda(edge_list_path, roi, output_dir, cutoff)

"""
print("Plotting and saving persistence diagrams...")
plot_save_diagrams(diagrams, roi, output_dir)
"""

# Extract H1 features and persistence values
h1 = diagrams[1]
persistence = h1[:, 1] - h1[:, 0]

# Threshold H1 features by persistence > 0 (or change cutoff if desired)
significant_features = h1[persistence > 0]

# Save persistence diagrams and features
np.save(os.path.join(output_dir, f"{roi}_H1_features.npy"), significant_features)
with open(os.path.join(output_dir, f"{roi}_cutoff.txt"), "w") as f:
    f.write(str(cutoff))

print("Pipeline complete!")

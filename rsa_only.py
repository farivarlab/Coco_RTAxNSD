import numpy as np
import pandas as pd
from os.path import join
import scipy.stats as stats
import gc

# === Constants ===
base_path = "data"
selected_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"]

def compare_rdms_subsampled(rdm1_path, rdm2_path, n_samples=10000, seed=42):
    rdm1 = np.load(rdm1_path, mmap_mode='r')
    rdm2 = np.load(rdm2_path, mmap_mode='r')

    assert rdm1.shape == rdm2.shape
    n = rdm1.shape[0]

    rng = np.random.default_rng(seed)
    idx = rng.choice(n, size=min(n_samples, n), replace=False)

    # Extract sub-RDMs
    sub1 = rdm1[np.ix_(idx, idx)]
    sub2 = rdm2[np.ix_(idx, idx)]

    # Get upper triangle
    mask = np.triu(np.ones_like(sub1), k=1).astype(bool)
    return stats.spearmanr(sub1[mask], sub2[mask])[0]



# === RSA computation ===
n = len(selected_rois)
rsa_matrix = np.zeros((n, n))

for i in range(n):
    rdm_i_path = join(base_path, f"{selected_rois[i]}_RDM.npy")
    for j in range(i, n):
        rdm_j_path = join(base_path, f"{selected_rois[j]}_RDM.npy")
        rsa_score = compare_rdms_subsampled(rdm_i_path, rdm_j_path)
        rsa_matrix[i, j] = rsa_score
        rsa_matrix[j, i] = rsa_score
        gc.collect()

np.save(join(base_path, "rsa_matrix.npy"), rsa_matrix)
print("✅ RSA matrix saved successfully.")

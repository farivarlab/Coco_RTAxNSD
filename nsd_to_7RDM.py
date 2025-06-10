from os.path import expanduser, join
import nibabel as nib
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from scipy.stats import rankdata


# === Constants ===
base_path = "data"
roi_path = "lh.HCP_MMP1.mgz"
roi_labels_txt = "HCP_MMP1.mgz.txt"
selected_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"] 

# === Helper Methods ===


def compute_rdm(matrix, chunk_size=5000):
    """
    Compute a Spearman-based RDM from a large matrix using chunking.
    Assumes `matrix` shape = (n_samples, n_features)
    
    Parameters:
        matrix (ndarray): The full matrix to compute RDM from
        chunk_size (int): Number of rows to process per block

    Returns:
        rdm (ndarray): The full RDM (correlation distance matrix)
    """
    n_samples = matrix.shape[0]
    print(f"🔍 Chunked RDM computation: {n_samples} × {n_samples} (chunk_size = {chunk_size})")
    
    # Step 1: Rank-transform the matrix row-wise (Spearman)
    print("🔁 Applying rank transform row-wise...")
    ranked = np.empty_like(matrix, dtype=np.float32)
    for i in range(n_samples):
        ranked[i] = rankdata(matrix[i], method='average')
        if i % 1000 == 0:
            print(f"  ...ranked {i}/{n_samples}")

    # Step 2: Allocate empty RDM matrix
    rdm = np.empty((n_samples, n_samples), dtype=np.float32)

    # Step 3: Fill in RDM in chunks
    for i in range(0, n_samples, chunk_size):
        end_i = min(i + chunk_size, n_samples)
        block_i = ranked[i:end_i]

        for j in range(i, n_samples, chunk_size):
            end_j = min(j + chunk_size, n_samples)
            block_j = ranked[j:end_j]

            # Compute correlation distances (1 - Spearman) for this block
            d_block = pairwise_distances(block_i, block_j, metric="correlation")

            # Assign to appropriate slice
            rdm[i:end_i, j:end_j] = d_block
            if i != j:
                rdm[j:end_j, i:end_i] = d_block.T  # fill symmetric half

            print(f"  ✅ Block [{i}:{end_i}, {j}:{end_j}] done")

    print("✅ Finished computing chunked RDM")
    return rdm
    

def compare_rdms(rdm1, rdm2):
    mask = np.triu(np.ones_like(rdm1), k=1).astype(bool)
    return stats.spearmanr(rdm1[mask], rdm2[mask])[0]



def compute_and_save_roi_rdms(base_path, roi_path, roi_labels_txt, selected_rois, n_sessions=40, download_npy=False):
    roi_mgh = nib.load(roi_path).get_fdata().squeeze()
    roi_df = pd.read_csv(roi_labels_txt, sep=" ", header=None, names=["label", "name"])
    roi_dict = {row["name"]: row["label"] for _, row in roi_df.iterrows()}
    roi_responses = {roi: [] for roi in selected_rois}

    for session_idx in range(1, n_sessions + 1):
        beta_file = join(base_path, f"lh.betas_session{session_idx:02d}.mgh")
        try:
            betas = nib.load(beta_file).get_fdata().astype(np.float32)
        except FileNotFoundError:
            print(f"❌ Session {session_idx:02d} not found. Skipping.")
            continue
        betas = betas.squeeze().T  # (n_images, n_nodes)
        for roi in selected_rois:
            roi_label = roi_dict.get(roi)
            if roi_label is None:
                print(f"❌ ROI label not found for {roi}")
                continue

            roi_indices = np.where(roi_mgh == roi_label)[0]
            if len(roi_indices) == 0:
                print(f"❌ No vertices found for ROI {roi}")
                continue

            roi_betas = betas[:, roi_indices].astype(np.float32)  # (n_images, n_roi_nodes)
            roi_responses[roi].append(roi_betas)
            print(f"✅ Accumulated data across {session_idx} sessions for {roi}")
    
    
    # Compute RDMs and save
    
    for i, roi in enumerate(selected_rois):
        if len(roi_responses[roi]) == 0:
            print(f"⚠️ No data collected for ROI {roi}")
            continue

        all_data = np.vstack(roi_responses[roi]).astype(np.float32)  # (n_total_images, n_roi_nodes)
        print(f"{roi}: concatenated shape = {all_data.shape}")
        
        rdm = compute_rdm(all_data, chunk_size=5000)
        
        if download_npy:
            np.save(join(base_path, f"{roi}_RDM.npy"), rdm)
        
        del rdm, all_data
        import gc
        gc.collect()
        
        print(f"📁 Computed RDM for {roi}")



# === Call the method ===
compute_and_save_roi_rdms(base_path, roi_path, roi_labels_txt, selected_rois, download_npy=True)
    

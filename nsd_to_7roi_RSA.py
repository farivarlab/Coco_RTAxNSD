from os.path import expanduser, join
import nibabel as nib
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances

# === Constants ===
base_path = expanduser("~/NSD_cogsci/data")
base_path_roi = expanduser("~/NSD_cogsci")
roi_path = join(base_path_roi, "lh.HCP_MMP1.mgz")
roi_labels_txt = join(base_path_roi, "HCP_MMP1.mgz.txt")
selected_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"] 

# === Helper Methods ===
from scipy.stats import rankdata
from sklearn.metrics import pairwise_distances

def compute_rdm(matrix, indices=None):
    sampled_matrix = matrix[indices, :]
    # Rank each row individually (Spearman step)
    ranked = np.apply_along_axis(rankdata, 1, sampled_matrix)
    # Then use Pearson on the ranked matrix to get Spearman distances
    rdm = pairwise_distances(ranked, metric='correlation')
    return rdm, indices
    

def compare_rdms(rdm1, rdm2):
    mask = np.triu(np.ones_like(rdm1), k=1).astype(bool)
    return stats.spearmanr(rdm1[mask], rdm2[mask])[0]



def compute_and_save_roi_rdms(base_path, roi_path, roi_labels_txt, selected_rois, n_sessions=40, download_npy=False):
    roi_mgh = nib.load(roi_path).get_fdata().squeeze()
    roi_df = pd.read_csv(roi_labels_txt, sep=" ", header=None, names=["label", "name"])
    roi_dict = {row["name"]: row["label"] for _, row in roi_df.iterrows()}
    roi_responses = {roi: [] for roi in selected_rois}
    # going to be returned:
    roi_rmds = {}
    n_samples = 5000 # change downsample size
    total_images = 30000
    np.random.seed(42)
    selected_indices = np.random.choice(total_images, size=n_samples, replace=False)


    for session_idx in range(1, n_sessions + 1):
        beta_file = join(base_path, f"lh.betas_session{session_idx:02d}.mgh")
        try:
            betas = nib.load(beta_file).get_fdata()
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

            roi_betas = betas[:, roi_indices]  # (n_images, n_roi_nodes)
            roi_responses[roi].append(roi_betas)
            print(f"✅ Accumulated data across {session_idx} sessions for {roi}")
    
    
    # Compute RDMs and plot all in one figure
    n_rois = len(selected_rois)
    ncols = 4
    nrows = int(np.ceil(n_rois / ncols))

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols, 4*nrows))
    axes = axes.flatten()

    for i, roi in enumerate(selected_rois):
        if len(roi_responses[roi]) == 0:
            print(f"⚠️ No data collected for ROI {roi}")
            continue

        all_data = np.vstack(roi_responses[roi])  # (n_total_images, n_roi_nodes)
        print(f"{roi}: concatenated shape = {all_data.shape}")
        
        rdm, _ = compute_rdm(all_data, indices=selected_indices)
        roi_rmds[roi] = rdm

        if download_npy:
            np.save(join(base_path, f"RDM_{roi}.npy"), rdm)

        ax = axes[i]
        sns.heatmap(rdm, cmap='viridis', ax=ax, cbar=False)
        ax.set_title(f"{roi}")
        ax.axis('off')

        print(f"📁 Computed RDM for {roi}")
        
    # Remove any empty subplots
    for j in range(i+1, nrows*ncols):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(join(base_path, "All_RDMs_combined.png"))
    plt.show()
    
    return roi_rmds

# === Call the method ===
roi_rdms = compute_and_save_roi_rdms(base_path, roi_path, roi_labels_txt, selected_rois)
print(len(roi_rdms))
print(len(roi_rdms.get("V1")))

# Compute RSA on 7 big RDMs
n = len(selected_rois)
rsa_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i <= j:
            rsa_score = compare_rdms(roi_rdms[selected_rois[i]], roi_rdms[selected_rois[j]])
            rsa_matrix[i, j] = rsa_score
            rsa_matrix[j, i] = rsa_score
# Optionally convert to DataFrame for nice labels
rsa_df = pd.DataFrame(rsa_matrix, index=selected_rois, columns=selected_rois)

# Show or save heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(rsa_df, annot=True, cmap="coolwarm", vmin=0, vmax=1)
plt.title("RSA (Spearman) between ROIs")
plt.tight_layout()
plt.show()            

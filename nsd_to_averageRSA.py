from os.path import expanduser, join
import nibabel as nib
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt


# === 1. load data files ===
base_path = expanduser("~/NSD_cogsci/data")
base_path_roi = expanduser("~/NSD_cogsci")
roi_path = join(base_path_roi,"lh.HCP_MMP1.mgz")
roi_labels_txt = join(base_path_roi, "HCP_MMP1.mgz.txt")
selected_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"] 

session_rdms = []  # Store each session's full ROI RDM
rsa_matrices = []  # Optional: store RSA comparisons per session

# === helper methods ===
def compute_rdm(matrix):
        rho, _ = stats.spearmanr(matrix, axis=0)
        return 1 - rho  # Convert to distance
    
def compare_rdms(rdm1, rdm2):
        mask = np.triu(np.ones_like(rdm1), k=1).astype(bool)
        return stats.spearmanr(rdm1[mask], rdm2[mask])[0]
    
    
    
# === start looping! ===
for session_idx in range(1, 41):
    # === 2. load beta matrix ===
    session_filename = f"lh.betas_session{session_idx:02d}.mgh"
    session_path = join(base_path, session_filename)
    
    beta_img = nib.load(session_path)
    beta_data = beta_img.get_fdata().reshape(-1, beta_img.shape[-1]) #(163842, 750)
    print(beta_data.shape, ". Shape should be (163842, 750)")

    # === 3. load ROI mapping ===
    roi_img = nib.load(roi_path)
    roi_data = np.squeeze(roi_img.get_fdata()).astype(int)
    print(roi_data.shape, ". Shape should be (163842, )")

    # === 4. load ROI names ===
    roi_mapping = {}
    with open(roi_labels_txt, "r") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                roi_mapping[int(parts[0])] = parts[1]

    roi_names = np.array([roi_mapping.get(r, "Unknown") for r in roi_data])
    print("all roi_names: ", roi_names, roi_names.shape, " names in total")

    # === 5. filter data to selected ROIs only ===
    roi_mask = np.isin(roi_names, selected_rois)
    roi_names_selected = roi_names[roi_mask]
    beta_selected = beta_data[roi_mask]

    print("Selected ROIs: ", roi_names_selected, "\n Shape after filtering: ", beta_selected.shape)

    # === 6. order data per ROI ===
    roi_data_dict = {
        roi: beta_selected[roi_names_selected == roi]
        for roi in selected_rois
        if np.any(roi_names_selected == roi) #so that data are grouped by ROIs
    }
    print("roi_data_dict[\"V1\"] (nodes that belong to V1): ", roi_data_dict["V1"].shape)


    # 🔹 7. Compute RDMs (Spearman correlation distance)

    roi_rdms = {}
    for roi, mat in roi_data_dict.items():
        rdm = compute_rdm(mat)
        roi_rdms[roi] = rdm
        print(f"✅ RDM computed for ROI: {roi}")
        session_rdms.append(roi_rdms)


    # ⚠️ 8. plot RDMs in one figure (Spearman correlation distance）
    num_rois = len(roi_rdms)
    """
    cols = 4
    rows = -(-num_rois // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    axes = axes.flatten()

    for i, (roi, rdm) in enumerate(roi_rdms.items()):
        sns.heatmap(rdm, ax=axes[i], cmap="viridis", square=True, cbar=False)
        axes[i].set_title(f"{roi} RDM")
        axes[i].set_xlabel("Stimuli")
        axes[i].set_ylabel("Stimuli")

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle("Representational Dissimilarity Matrices (RDMs)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    """

    # === 9. 😆 RSA: time to compare all RDMs! ===
    

    rsa_matrix = np.zeros((num_rois, num_rois))
    valid_rois = list(roi_rdms.keys())

    for i, roi1 in enumerate(valid_rois):
        for j, roi2 in enumerate(valid_rois):
            rsa_matrix[i, j] = 1.0 if i == j else compare_rdms(roi_rdms[roi1], roi_rdms[roi2])
    
    rsa_matrices.append({
        "session": session_idx,
        "rsa_matrix": rsa_matrix,
        "rois": valid_rois
    })
    # === Plot RSA Matrix ===
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(rsa_matrix, annot=True, xticklabels=valid_rois, yticklabels=valid_rois,
                cmap="coolwarm", vmin=0, vmax=1)
    plt.title("RSA Similarity Between Selected ROIs (Spearman)")
    plt.tight_layout()
    plt.show()
    """
    # Save RDMs and RSA matrices for future use
    np.save(join(base_path, "all_session_rdms.npy"), session_rdms)
    np.save(join(base_path, "all_session_rsa_matrices.npy"), rsa_matrices)


    print(f"✅ Session {session_idx:02d} processed.")
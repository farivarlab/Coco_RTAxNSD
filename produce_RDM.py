import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# Load the precomputed matrix
csv_path = "beta_matrix_new_roi.csv"  # Update with actual file path
df = pd.read_csv(csv_path)

roi_column = df.iloc[:, 0]  # First column: ROI labels
node_column = df.iloc[:, 1]  # Second column: Node indices
data_matrix = df.iloc[:, 2:].to_numpy()  # Remaining columns: condition data


# 🔹 Remove duplicates & filter valid ROIs
unique_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"] 
valid_rois = [roi for roi in unique_rois if roi in roi_column.unique()]

if not valid_rois:
    raise ValueError("No valid ROIs found in dataset!")

# 🔹 Extract data for each valid ROI
roi_data = {roi: data_matrix[roi_column == roi, :] for roi in valid_rois}

# 🔹 Compute RDMs (Spearman correlation distance)
def compute_rdm(matrix):
    rho, _ = stats.spearmanr(matrix, axis=0)
    return 1 - rho  # Convert to distance

roi_rdms = {roi: compute_rdm(matrix) for roi, matrix in roi_data.items()}

#save each rdms as a csv file
for roi, matrix in roi_data.items():
    rdm = compute_rdm(matrix)
    roi_rdms[roi] = rdm
    # Save RDM to CSV
    np.savetxt(f"RDMs/{roi}_RDM.csv", rdm, delimiter=",")
    print(f"saved {roi}_RDM to /Users/magico/RDMs/")

#⚠️plot RDMs in one figure (Spearman correlation distance）

num_rois = len(valid_rois)
cols = 4  # Define number of columns in subplot grid
rows = -(-num_rois // cols)  # Compute number of rows (ceil division)

fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))  # Adjust figure size
axes = axes.flatten()  # Flatten in case we have extra subplots

for i, (roi, rdm) in enumerate(roi_rdms.items()):
    sns.heatmap(rdm, cmap="viridis", square=True, ax=axes[i])
    axes[i].set_title(f"{roi} RDM")
    axes[i].set_xlabel("Conditions")
    axes[i].set_ylabel("Conditions")

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.suptitle("Representational Dissimilarity Matrices (RDMs)", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()





# 🔹 Compute RSA (pairwise RDM similarity)
def compare_rdms(rdm1, rdm2):
    mask = np.triu(np.ones(rdm1.shape), k=1).astype(bool)
    return stats.spearmanr(rdm1[mask], rdm2[mask])[0]  

rsa_matrix = np.zeros((len(valid_rois), len(valid_rois)))
for i, roi1 in enumerate(valid_rois):
    for j, roi2 in enumerate(valid_rois):
        rsa_matrix[i, j] = 1.0 if i == j else compare_rdms(roi_rdms[roi1], roi_rdms[roi2])



# 🔹 Plot only the final RSA heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(rsa_matrix, annot=True,  xticklabels=valid_rois, yticklabels=valid_rois, cmap="coolwarm", vmin=0, vmax=1)
plt.title("RSA Similarity Between Selected ROIs (Spearman)")
plt.show()

# 🔹 Close all unnecessary figures to free memory
plt.close('all')
print("Done!")

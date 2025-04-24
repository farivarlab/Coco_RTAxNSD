import nibabel as nib
import pandas as pd
import numpy as np

# Load the MGH file
img = nib.load("/Users/magico/Downloads/lh.betas_session01.mgh")
data = img.get_fdata()

# Reshape to (num_nodes, num_conditions)
data_reshaped = data.reshape(-1, data.shape[-1])

# Generate dummy ROI labels (replace this with real ROI mapping later)
num_nodes = data_reshaped.shape[0]

#extract ROI labels
roi_img = nib.load("/Users/magico/Downloads/lh.HCP_MMP1.mgz")
roi_data = np.squeeze(roi_img.get_fdata())

unique_rois = np.unique(roi_data)
print("Unique ROI labels:", unique_rois)

# Load the ROI label mapping
roi_mapping = {}
with open("/Users/magico/Downloads/HCP_MMP1.mgz.txt", "r") as f:
    for line in f:
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            roi_mapping[int(parts[0])] = parts[1]

node_indices = np.arange(num_nodes)  # Node indices
roi_names = np.array([roi_mapping.get(int(label), "Unknown") for label in roi_data])


df = pd.DataFrame(data_reshaped)
df.insert(0, "Node_Index", node_indices)
df.insert(0, "ROI", roi_names)

# Save as CSV
csv_path = "/Users/magico/beta_matrix_new_roi.csv"
df.to_csv(csv_path, index=False)

print(f"CSV matrix with ROIs saved at: {csv_path}")
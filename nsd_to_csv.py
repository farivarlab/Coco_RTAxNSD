from os.path import expanduser, join
import nibabel as nib
import pandas as pd
import numpy as np

# Don't need to run if you don't need csv file
# Load the MGH file
base_path = expanduser("~/NSD_cogsci")
img = nib.load(join(base_path, "lh.betas_session02.mgh"))
data = img.get_fdata()

# Reshape to (num_nodes, num_conditions)
data_reshaped = data.reshape(-1, data.shape[-1])

# Generate dummy ROI labels (replace this with real ROI mapping later)
num_nodes = data_reshaped.shape[0]

#extract ROI labels
roi_img = nib.load(join(base_path,"lh.HCP_MMP1.mgz"))
roi_data = np.squeeze(roi_img.get_fdata())

unique_rois = np.unique(roi_data)
print("Unique ROI labels:", unique_rois)

# Load the ROI label mapping
roi_mapping = {}
with open(join(base_path, "HCP_MMP1.mgz.txt"), "r") as f:
    for line in f:
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            roi_mapping[int(parts[0])] = parts[1]

node_indices = np.arange(num_nodes)  # Node indices
roi_names = np.array([roi_mapping.get(int(label), "Unknown") for label in roi_data])


df = pd.DataFrame(data_reshaped)
df.insert(0, "Node_Index", node_indices)
df.insert(0, "ROI", roi_names)
print (df.shape) #⚠️ should be (163842, 752)
# Save as CSV
csv_path = join(base_path, "beta_matrix_new_roi02.csv")
df.to_csv(csv_path, index=False)

print(f"CSV matrix with ROIs saved at: {csv_path}")
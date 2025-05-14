import nibabel as nib
import os

# Assuming local or mounted path to MGH files from S3
beta_dir = "/Users/magico/NSD_cogsci/data/"
# Check the shape of session 1-40 of subject 1
for i in range(1, 41):
    file_path = os.path.join(beta_dir, f"lh.betas_session{i:02d}.mgh")
    img = nib.load(file_path)
    data = img.get_fdata()
    print(f"Session {i:02d}: shape = {data.shape}")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join
import math

# === Constants ===
base_path = "data"
rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"]

def plot_rsa_heatmap(base_path=base_path, rois=rois, rsa_filename="rsa_matrix.npy", save_as="rsa_heatmap.png"):
    """
    Loads an RSA matrix from disk and plots a heatmap with labeled ROIs.

    Parameters:
        base_path (str): Directory where the RSA .npy file is stored and output image will be saved.
        rois (list of str): List of ROI names in correct order.
        rsa_filename (str): Name of the RSA matrix file (default: "rsa_matrix.npy").
        save_as (str): Filename for the output image (default: "rsa_heatmap.png").
    """
    # Load RSA matrix
    rsa_path = join(base_path, rsa_filename)
    rsa_matrix = np.load(rsa_path)

    # Convert to DataFrame for labeling
    rsa_df = pd.DataFrame(rsa_matrix, index=rois, columns=rois)

    # Plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(rsa_df, annot=True, cmap="coolwarm", vmin=0, vmax=1)
    plt.title("RSA (Spearman) between ROIs")
    plt.tight_layout()

    # Save figure
    output_path = join(base_path, save_as)
    plt.savefig(output_path)
    plt.show()
    print(f"✅ RSA heatmap saved to: {output_path}")


def plot_all_rdms(base_path=base_path, rois=rois, preview_size=1000, save_path="all_RDMs_preview.png"):
    """
    Plots the top-left preview of each ROI's RDM in a grid and saves the figure.

    Parameters:
        base_path (str): Path to the folder containing RDM .npy files.
        rois (list of str): List of ROI names corresponding to RDM file prefixes.
        preview_size (int): Number of rows/cols to visualize from each RDM (default: 1000).
        save_path (str): Filename to save the final plot (relative to base_path).
    """
    n_rois = len(rois)
    ncols = 4
    nrows = math.ceil(n_rois / ncols)

    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows))
    axes = axes.flatten()

    for i, roi in enumerate(rois):
        try:
            rdm_path = join(base_path, f"{roi}_RDM.npy")
            rdm = np.load(rdm_path, mmap_mode='r')  # memory-mapped to reduce RAM use
            rdm_preview = rdm[:preview_size, :preview_size]

            ax = axes[i]
            sns.heatmap(rdm_preview, cmap="viridis", cbar=False, ax=ax)
            ax.set_title(f"{roi} (top {preview_size}×{preview_size})")
            ax.axis("off")
        except Exception as e:
            print(f"⚠️ Failed to load or plot RDM for {roi}: {e}")
            fig.delaxes(axes[i])  # remove failed subplot if applicable

    # Remove unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    output_path = join(base_path, save_path)
    plt.savefig(output_path)
    plt.show()
    print(f"✅ Saved combined RDM preview to: {output_path}")

plot_rsa_heatmap()
plot_all_rdms()
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import expanduser, join
from matplotlib import gridspec

selected_rois = ["V1", "V2", "V3", "V4", "V8", "LO2", "PIT"] 

# Load RDMs
# session index start from 1
def loadSingleRDM(roi_name, session_idx):
    basepath = expanduser("~/NSD_cogsci/data")
    all_rdms = np.load(join(basepath, "all_session_rdms.npy"), allow_pickle=True)  # list of dicts
    roi_name = roi_name
    session_idx = session_idx-1  # session 1

    rdm = all_rdms[session_idx][roi_name]  # (750, 750)

    plt.figure(figsize=(8, 6))
    sns.heatmap(rdm, cmap="viridis")
    plt.title(f"RDM for ROI: {roi_name}, Session: {session_idx+1}")
    plt.xlabel("Stimulus")
    plt.ylabel("Stimulus")
    plt.show()
    
def loadSingleRSA(session_idx):
    basepath = expanduser("~/NSD_cogsci/data")
    # Load RSAs
    rsa_data = np.load(join(basepath, "all_session_rsa_matrices.npy"), allow_pickle=True)
    rsa_dict = rsa_data[session_idx-1]  # session 1

    plt.figure(figsize=(6, 5))
    sns.heatmap(rsa_dict["rsa_matrix"], xticklabels=rsa_dict["rois"], yticklabels=rsa_dict["rois"], 
                annot=True, cmap="coolwarm", vmin=0, vmax=1)
    plt.title(f"RSA Matrix - Session {rsa_dict['session']}")
    plt.show()
    
def plotAllRSA():
    basepath = expanduser("~/NSD_cogsci/data")
    rsa_data = np.load(join(basepath, "all_session_rsa_matrices.npy"), allow_pickle=True)

    num_sessions = len(rsa_data)
    ncols = 10  # columns in figure
    nrows = (num_sessions + ncols - 1) // ncols

    fig, axs = plt.subplots(nrows, ncols, figsize=(ncols*2.2, nrows*2.2))
    axs = axs.flatten()

    for i, rsa_dict in enumerate(rsa_data):
        ax = axs[i]
        sns.heatmap(rsa_dict["rsa_matrix"], 
                    xticklabels=False, yticklabels=False,  # Optional: hide labels for space
                    cbar=False, vmin=0, vmax=1,
                    cmap="coolwarm", ax=ax)
        ax.set_title(f"Sess {rsa_dict['session']}", fontsize=8)
        ax.axis('off')  # Optional: remove axis ticks

    # Turn off unused subplots
    for j in range(i + 1, len(axs)):
        axs[j].axis('off')

    plt.tight_layout()
    plt.suptitle("RSA Matrices Across All Sessions", fontsize=14, y=1.02)
    plt.subplots_adjust(top=0.94)
    plt.show()

def average40RSA():
    basepath = expanduser("~/NSD_cogsci/data")
    rsa_data = np.load(join(basepath, "all_session_rsa_matrices.npy"), allow_pickle=True)

    # Stack into 3D array (40, 7, 7)
    rsa_stack = np.stack([s["rsa_matrix"] for s in rsa_data], axis=0)
    mean_rsa = np.nanmean(rsa_stack, axis=0)  # shape: (7, 7)

    # Plot
    rois = rsa_data[0]["rois"]

    plt.figure(figsize=(6, 5))
    sns.heatmap(mean_rsa, xticklabels=rois, yticklabels=rois, cmap="coolwarm", vmin=0, vmax=1, annot=True)
    plt.title("Average RSA Matrix Across 40 Sessions")
    plt.show()

def plotAverageAndAllRSAs():
    basepath = expanduser("~/NSD_cogsci/data")
    rsa_data = np.load(join(basepath, "all_session_rsa_matrices.npy"), allow_pickle=True)

    # --- Prepare data ---
    rsa_stack = np.stack([s["rsa_matrix"] for s in rsa_data], axis=0)  # (40, 7, 7)
    mean_rsa = np.nanmean(rsa_stack, axis=0)
    rois = rsa_data[0]["rois"]
    num_sessions = len(rsa_data)

    # --- Plot setup ---
    fig = plt.figure(figsize=(20, 10))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3], wspace=0.05)

    # --- Left: Average RSA Matrix ---
    ax_avg = plt.subplot(gs[0])
    sns.heatmap(mean_rsa, xticklabels=rois, yticklabels=rois,
                annot=True, cmap="coolwarm", vmin=0, vmax=1, ax=ax_avg, cbar_kws={'shrink': 0.6})
    ax_avg.set_title("Average RSA Across 40 Sessions", fontsize=14)

    # --- Right: All 40 RSA matrices in grid ---
    grid_rows = 5
    grid_cols = 8
    inner_gs = gridspec.GridSpecFromSubplotSpec(grid_rows, grid_cols, subplot_spec=gs[1], wspace=0.15, hspace=0.25)

    for i, rsa_dict in enumerate(rsa_data):
        row = i // grid_cols
        col = i % grid_cols
        ax = plt.Subplot(fig, inner_gs[row, col])
        sns.heatmap(rsa_dict["rsa_matrix"], xticklabels=False, yticklabels=False,
                    cbar=False, cmap="coolwarm", vmin=0, vmax=1, ax=ax)
        ax.set_title(f"Session {rsa_dict['session']}", fontsize=7)
        ax.axis('off')
        fig.add_subplot(ax)

    plt.suptitle("RSA: Average (Left) and All Sessions (Right)", fontsize=16, y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
    
    


    
# playground
plotAverageAndAllRSAs()
loadSingleRDM("V3", 33)
loadSingleRSA(33)
# NSD_cogsci Dataset - Annotation & README  
**Author:** Coco  
**Date:** April 23, 2025  
**Lab:** Prof. Reza Farivar's Lab, McGill University  

---

## Project Summary  
This repository contains data and code used for topological similarty analysis (TSA) and representational similarity analysis (RSA) of the Natural Scenes Dataset (NSD) done as my Cognitive Science Honours Research Course. The project pecifically focuses on **beta values of surface-based fMRI data** from the **first session of Subject 1**. 

Analyses include generating ROI-based Representational Dissimilarity Matrices (RDMs), bootstrapping topological features, and stimulus-trial-matching for further Vietoris-Rips (VR) graph visualization.
### Important Links
- Documentation of `TDApplied` R package used during analysis: https://cran.r-project.org/web/packages/TDApplied/vignettes/ML_and_Inference.html
- Natural Scenes Dataset (NSD): https://naturalscenesdataset.org
- The following data from NSD are used for analysis. Download them from NSD following their file paths:
  - lh.betas_session01.mgh: `natural-scenes-dataset` > `nsddata_betas` > `ppdata` > `subj01` > `fsaverage` > `betas_fithrf`
  - nsd_stimuli.hdf5: `natural-scenes-dataset` > `nsddata_stimuli` > `stimuli` > `nsd`


---

## Folder

### `RDMs/`  
Contains 7 RDMs (Representational Dissimilarity Matrices) produced by `produce_RDM.py`.  
- Format: CSV  
- Naming Convention: `[ROI]_RDM.csv` (e.g., `LO2_RDM.csv`)  
- Content: Symmetric matrices containing pairwise Spearman correlation distances (1 - Spearman ρ) between trials within a given ROI (7 ROIs are chosen in this case).
- ROIs chosen: Primary Visual Cortex (V1), Second Visual Area (V2), Third Visual Area (V3), Fourth Visual Area (V4), Eighth Visual Area (V8), Area Lateral Occipital 2 (Lo2), and Posterior-Infero-Temporal Complex (PIT).

### `report/`
Contains everything related to final report and poster for this project.
- `Coco_FinalReport_finalV.pdf`
- `Coco_poster_finalV.pdf`
- #### `results_plots/`
  - Includes all images and plots produced and used for analysis and final report




## Key Tables  

### `beta_matrix_new_roi.csv` (2.4GB)  
- Produced by running `nsd.py`
- Shape: `[#Nodes 163,842 x #Trials 750]`  
- Description: Beta values of Subject 1’s first session, matched to ROIs based on the `lh.HCP_MMP1.mgz` atlas.  
- Unit: fMRI beta values (no specific physical unit, normalized activation).  
- Each row = node/vertex (163,842), each column = image trial (750).

### `nsd_stim_info_merged.csv`  
- Contains important information about the matching between trial and NSD image stimuli  
- Purpose: Used for exploratory data analysis without ROI constraints.

### `Glasser_2016_Table.xlsx`  
- Atlas reference used for ROI labeling from `lh.HCP_MMP1.mgz`.  
- Includes descriptions and cortical locations of the 180 ROIs defined in the Glasser HCP-MMP1.0 parcellation.

### `subj1_trial_mapping.csv`  
- Contains the trial to NSD image ID mapping for subj1.
- 2 Columns:  
  - `trial_number`: trial index used in scripts  
  - `nsd_image_number`: image ID (0–72999) corresponding to NSD stimuli

---

## R 
**⚠️ Please only run the following R functions in given order.**

### `bootstrap_pd.r`  
Computes bootstrapped persistence diagrams for a given RDM.  
Useful for topological data analysis (TDA) and comparing topological features across ROIs.

### `rhdf5_stimuli.r`  
- Reads from `nsd_stimuli.hdf5`  
- Matches trials to the actual image stimuli  
- Can visualize image snippets corresponding to selected trials / features / representative cycles

### `plotVR.r`  
Plots a single VR graph combining all topological features of a given RDM.

### `plotVR_separate.r`  (optional)
Generates separate VR (Vietoris-Rips) graphs for each topological feature (e.g., 0D, 1D holes) of a given RDM.



---

## Python  

### `nsd_stim_info_transfer.py`  
- Inputs: `nsd_stim_info_merged.csv`
- Outputs: None  
- Task: Transfers the beta values table to Azure Data Studio SQL Server database for data preprocessing. 
  - `select_subject.sql`: SQL query that will select all information regarding the chosen subject
  - `subj1_trial_mapping.sql`: SQL query that will produce trial to NSDid matching of chosen subject (`subj1_trial_mapping.csv`)

### `nsd.py`  
- Inputs: `lh.betas_session01.mgh`, `lh.HCP_MMP1.mgz`  
- Outputs: `beta_matrix_new_roi.csv`  
- Task: Matches node-wise beta values to cortical ROIs using the HCP_MMP1 atlas and stores into a new csv

### `nsdtransfer.py`  
- Inputs: `beta_matrix_new_roi.csv` (by running `nsd.py`)
- Outputs: None  
- Task: Transfers the beta values table to Azure Data Studio SQL Server database for data inspection and manipulation.


### `produce_RDM.py`  
- Input: `beta_matrix_new_roi.csv` (by running `nsd.py`)
- Output: 7 ROI-based RDMs (CSV)  
- Metric: Spearman correlation distance (1 - ρ)
- Task: produce RDMs given selected ROIs (7 are selected here) based on Spearman correlation distance

### `readpkl.py`  
Reads `nsd.experiment.mat` in MATLAB `.mat` format.  
- Purpose: Accesses metadata such as timing, image presentation order, etc.

---

## Other 

### `nsd_expdesign.mat`  
- MATLAB file  
- Contains full NSD experimental design metadata  
- Useful for aligning image presentation with trials and conditions

### `lh.betas_session01.mgh`  
- Original surface-based beta data for Subject 1, Session 1  
- Used as the raw data input for all downstream beta extraction

### `nsd_stimuli.hdf5`  
- HDF5 file containing all 73,000 NSD image stimuli  
- Used for trial-to-image mapping based on specific repetition pattern and visualization tasks

### `lh.HCP_MMP1.mgz`  
- Used to label brain surface nodes with 180 ROIs

---

## 📝 Notes  
- `.Rprofile`: Prevents VSCode from triggering unnecessary linter warnings related to `lintr.linters`. Not related to analysis.  
- All file paths should be updated with relative paths.
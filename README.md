# NSD_cogsci Dataset - Annotation & README  
**Author:** Coco Wang  
**Date:** April 23, 2025   
**Lab:** Prof. Reza Farivar's Lab, McGill University  

---

## Project Summary  
This repository contains data and scripts used for Representational topology analysis (RTA) and representational similarity analysis (RSA) of the Natural Scenes Dataset (NSD) done as my Cognitive Science Honours Research Course (COG 444). The project specifically focuses on **beta values of surface-based fMRI data** from the **40 sessions of Subject 1**. 

Analyses include generating ROI-based Representational Dissimilarity Matrices (RDMs), bootstrapping topological features of Persistence Diagrams (PD), and stimulus-trial-matching for further Vietoris-Rips (VR) graph visualization.
### Important Links
- Documentation of `TDApplied` R package used during analysis: https://cran.r-project.org/web/packages/TDApplied/vignettes/ML_and_Inference.html
- Natural Scenes Dataset (NSD): https://naturalscenesdataset.org
- The following large dataset from NSD are used for analysis. Download them from NSD following their file paths:
  - lh.betas_session01.mgh: `natural-scenes-dataset` > `nsddata_betas` > `ppdata` > `subj01` > `fsaverage` > `betas_fithrf`
  - nsd_stimuli.hdf5: `natural-scenes-dataset` > `nsddata_stimuli` > `stimuli` > `nsd`


---

## Folder

### `report/`
Contains everything related to final report and poster for this project.
- `Coco_Final_Report_202506_.pdf`
- `Coco_poster_finalV.pdf`
- #### `results_plots/`
  - Includes all images and plots produced and used for analysis and final report




## Key Tables  

### `nsd_stim_info_merged.csv`  
- Contains important information about the matching between trial and NSD image stimuli  
- Purpose: Used for exploratory data analysis without ROI constraints.

### `Glasser_2016_Table.xlsx`  
- Atlas reference used for ROI labeling from `lh.HCP_MMP1.mgz`.  
- Includes descriptions and cortical locations of the 180 ROIs defined in the Glasser HCP-MMP1.0 parcellation.

### `subj1_trial_mapping.csv`  
- Contains the trial to NSD image ID mapping for Subject 1.
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

### `plotVR_separate.r`  _(optional)_
Generates separate VR (Vietoris-Rips) graphs for each topological feature (e.g., 0D, 1D holes) of a given RDM.



---

## Python 
### 1. 🌟 To calculate your data:


#### `nsd_to_RDM_RSA_single.py`  
- Scale: single trial of Subject 1 (163,842 x 750)
- Input: `beta_matrix_new_roi.csv`
- Output: 7 ROI-based RDMs (CSV), 1 RSA matrices 
- Metric: Spearman correlation distance (1 - ρ)
- Task: produce RDMs given selected ROIs (7 are selected here) based on Spearman correlation distance on a single session of a subject. AND perform RSA on the given ROIs.

#### `nsd_to_7RDM.py` 
- Scale: 40 trial of Subject 1 (163,842 x 750 x 40) 
- Input: `\data\lh.betas_session*.csv`
- Output: 7 big ROI-based RDMs at `data/{rois}_RDM.npy`
- Metric: Spearman correlation distance (1 - ρ)

#### `7RDM_RSA.py` 
- Scale: 7 RDMs calculated over 40 trial of Subject 1 (7 x 30,000 x 30,000) 
- Input: 7 `{rois}_RDM.npy` calculated from `nsd_to_7RDM.py`
- Output: `rsa_matrix.npy` across 7 RDMs

👉 Use `plot_matrix.py` below for RSA and RDM visualization.

### 2. To read/ transfer your data:
#### `plot_matrix.py`  
- Inputs: `{roi}_RDM.npy` calculated from `nsd_to_7RDM.py`
- Outputs: rsa_heatmap.png from `plot_rsa_heatmap()`, `plot_all_rdms()`
- Task: Visualize the RSA npy matrix as a heatmap

#### `nsd_stim_info_transfer.py`  
- Scale: single trial of Subject 1 (163,842 x 750)
- Inputs: `nsd_stim_info_merged.csv`
- Outputs: None  
- Task: Transfers the beta values table to Azure Data Studio SQL Server database for data preprocessing. 
  - `select_subject.sql`: SQL query that will select all information regarding the chosen subject
  - `subj1_trial_mapping.sql`: SQL query that will produce trial to NSDid matching of chosen subject (`subj1_trial_mapping.csv`)


#### `nsdtransfer.py`  
- Scale: single trial of Subject 1 (163,842 x 750)
- Inputs: `beta_matrix_new_roi.csv`
- Outputs: None  
- Task: Transfers the beta values table to Azure Data Studio SQL Server database for data inspection and manipulation.


### 3. Helper functions:

#### `nsd_to_csv.py` 
- Scale: single trial of Subject 1 (163,842 x 750) 
- Inputs: `lh.betas_session01.mgh`, `lh.HCP_MMP1.mgz`  
- Outputs: `beta_matrix_new_roi.csv`  _(table already provided)_
- Task: Matches node-wise beta values to cortical ROIs using the HCP_MMP1 atlas and stores into a new csv

#### `checkShape.py`  
- Scale: 40 trial of Subject 1 (163,842 x 750 x 40)
- Purpose: Inspect the shape of the files saved under /data

#### `readpkl.py`  
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

## Notes  
- All file paths should be updated with relative paths.

## References
1. Kriegeskorte, N., Mur, M., and Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. Front. systems neuroscience 2, 4. https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/neuro.06.004.2008/full
2. Brown, S., & Farivar, R. (2024). The Topology of Representational Geometry. bioRxiv, 2024-02.https://www.biorxiv.org/content/10.1101/2024.02.16.579506v1
3. Allen, E.J., St-Yves, G., Wu, Y. et al. (2022). A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence.Nat Neurosci 25, 116–126. https://doi.org/10.1038/s41593-021-00962-x
4. Atlases — neuroimaging core 0.1.1 documentation. (n.d.). Retrieved from https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/atlases.html#id4
5. Brown, S., & Farivar, R. (2025, January 20). Machine Learning and Inference for Topological Data Analysis. Retrieved from https://cran.r-project.org/web/packages/TDApplied/vignettes/ML_and_Inference.html
6. Pydory https://github.com/nihcompmed/Dory/tree/main
7. tdads https://github.com/shaelebrown/tdads/blob/main/src/tdads/PH_utils.py

library(TDApplied)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(TDA)
library(RcppCNPy)
library(reticulate)
library(RcppCNPy)

use_python("/home/nsd-lab/NSD_cogsci-main/.venv/bin/python", required = TRUE)
source_python("RTA_helpers.py")


rdm_files <- c("V1_RDM.npy", "V2_RDM.npy", "V3_RDM.npy", "V4_RDM.npy", "V8_RDM.npy", "LO2_RDM.npy", "PIT_RDM.npy")
rdm_list <- lapply(rdm_files, function(file) {
  npyLoad(paste0("data/", file))
})

roi_names <- c("V1", "V2", "V3", "V4", "V8", "LO2", "PIT")
names(rdm_list) <- roi_names

#enclosing radius -> determine threshold
encl_radius_list <- lapply(rdm_list, enclosing_radius)
names(encl_radius_list) <- roi_names
print(encl_radius_list)
universal_null_rdm <- function(rdm_str){
  circ_result <- universal_null(rdm_list[[rdm_str]], thresh = enclosing_radius(rdm_list[[rdm_str]]))
  print(paste("Calculating null distribution of", rdm_str, "..."))
  return(circ_result)
}

#computing pd
ripser <- import_ripser()

# instead of filtering based on arbitrary persistence value
# we calculate bootstrapped persistence thresholds
# takes ~ 20min for one rdm matrix

bootstrap_rdm <- function(rdm_str){
  start.time <- Sys.time()
  set.seed(42)
  thresh <- bootstrap_persistence_thresholds(X = rdm_list[[rdm_str]],
                                           FUN_diag = 'ripsDiag',
                                           FUN_boot = 'ripsDiag',
                                           distance_mat = T,
                                           maxdim = 1,thresh = 2,num_workers = 2,
                                           alpha = 0.05,num_samples = 30,
                                           return_subsetted = T,return_pvals = T,
                                           calculate_representatives = T)
  diag <- thresh$diag
  par(mfrow = c(1,2))
  plot_diagram(diag,title = paste(rdm_str, " diagram"))

  plot_diagram(diag,title = paste(rdm_str, " diagram with thresholds"),
              thresholds = thresh$thresholds)
  
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  print(paste("done", rdm_str, "in", time.taken))
  return(thresh)
}
print("Start bootstrapping...")
thresh <- bootstrap_rdm("V1")
h1_features <- thresh$subsetted_diag # persistence values of each features
h1_cycles <- thresh$subsetted_representatives  #list of node indices that form the loops
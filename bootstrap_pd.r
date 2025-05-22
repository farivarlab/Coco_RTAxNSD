library(TDApplied)
library(dplyr)
library(ggplot2)
library("TDA")
library(gridExtra)


rdm_files <- c("V1_RDM.csv", "V2_RDM.csv", "V3_RDM.csv", "V4_RDM.csv", "V8_RDM.csv", "LO2_RDM.csv", "PIT_RDM.csv")
rdm_list <- lapply(rdm_files, function(file) 
    { as.matrix(read.csv(paste0("/Users/magico/NSD_cogsci/data/", file), header=FALSE))} )
roi_names <- c("V1", "V2", "V3", "V4", "V8", "LO2", "PIT")
names(rdm_list) <- roi_names


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
                                           alpha = 0.05,num_samples = 5,
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
# run after bootstarp_pd.r to check images of loops
library(rhdf5)
library(grid)
library(igraph)
library(RColorBrewer)

h5_file <- "/Users/magico/NSD_cogsci/nsd_stimuli.hdf5"
h5ls(h5_file)


subj1_trial_mapping <- read.csv("/Users/magico/NSD_cogsci/subj1_trial_mapping.csv", stringsAsFactors = FALSE)

# function to match node indices with image stimuli
map_nodes_to_nsdID <- function(nodes, mapping){
  mapped_images <- mapping$nsdID[match(nodes, mapping$trialID)]
  return(mapped_images)
}

h1_nsdIDs <- lapply(h1_cycles, function(cycle) {
  if (length(cycle) > 0) {
    map_nodes_to_nsdID(cycle, subj1_trial_mapping)
  } else {
    NA
  }
})

# print out nsdIDs for all features
for (i in seq_along(h1_nsdIDs)) {
  cat("\nH1 Feature", i, "corresponds to these nsdIDs:\n")
  print(h1_nsdIDs[[i]])
}


visualize_h1_images <- function(nsdIDs, ncol) {
  img_list <- lapply(nsdIDs, function(id) {
    img_array <- h5read(h5_file, "imgBrick", index = list(1:3, 1:425, 1:425, id))
    img_array <- drop(img_array)
    img_array <- aperm(img_array, c(3, 2, 1))  
    rasterGrob(as.raster(img_array))
  })
  
  # Arrange images in a grid layout
  grid.newpage()
  grid.arrange(grobs = img_list, ncol = ncol) 
}
# check one of the feature with images
visualize_h1_images(unique(h1_nsdIDs[[2]]), ncol = 3)




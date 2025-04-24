# run after bootstarp_pd.r, rhdf5_stimuli.r
rdm_str <- "V3"
rdm1 <- as.matrix(dist(rdm_list[[rdm_str]]))

valid_cycles <- h1_cycles #because we need exact trial indices, we don't filter empty cycles.
all_cycle_indices <- seq_along(h1_cycles)

cycle_colors <- rainbow(length(h1_cycles))
trials_of_interest <- unique(unlist(h1_cycles))
filtered_rdm <- rdm1[trials_of_interest, trials_of_interest, drop = FALSE]

node_cycle_map <- list()
node_colors <- rep(NA, length(trials_of_interest))  # Initialize empty color vector
names(node_colors) <- trials_of_interest  # Assign node names
for (cycle_idx in seq_along(valid_cycles)){
  cycle_nodes <- unique(as.vector(valid_cycles[[cycle_idx]]))
  for (node in cycle_nodes) {
    node_colors[as.character(node)] <- cycle_colors[cycle_idx]  # Assign cycle color
    node_cycle_map[[as.character(node)]] <- cycle_idx  # Store cycle index
  }
}



# plot vr graph with 
eps_1 <- max(h1_features$birth)/4
eps_2 <- (mean(h1_features$birth) + mean(h1_features$death))/2
full_vr_graph <- vr_graphs(X=filtered_rdm, distance_mat = TRUE, eps=c(eps_1, eps_2), return_clusters = TRUE)
layout <- plot_vr_graph(graphs=full_vr_graph, eps=eps_2, title=paste("VR Graph for Significant Features of", rdm_str), vertex_labels = FALSE, return_layout = TRUE, cols=node_colors, plot_isolated_vertices = TRUE)
# component_of = toString(h1_cycles[[1]][2])

image_size <- 0.05
for (i in rownames(layout)){
  nsd_id <- map_nodes_to_nsdID(i, subj1_trial_mapping)
  # Read image corresponding to NSD ID
  img_array <- h5read(h5_file, "imgBrick", index = list(1:3, 1:425, 1:425, nsd_id))
  img_array <- drop(img_array)
  img_array <- aperm(img_array, c(3, 2, 1))  # Convert to correct format
  img_raster <- as.raster(img_array)

  x_pos <- layout[as.character(i), 1L]
  y_pos <- layout[as.character(i), 2L]

  # Overlay image on graph node
  graphics::rasterImage(img_raster,
                        xleft = x_pos - image_size,
                        xright = x_pos + image_size,
                        ybottom = y_pos - image_size,
                        ytop = y_pos + image_size)
}

legend_labels <- sapply(all_cycle_indices, function(idx) {
  if (length(h1_cycles[[idx]]) == 0) {
    return("Empty")  # Mark empty cycles
  } else {
    return(paste0("Cycle ", idx))
  }
})

legend_colors <- sapply(all_cycle_indices, function(idx) {
  if (length(h1_cycles[[idx]]) == 0) {
    return("gray")  # Assign gray to empty cycles
  } else {
    return(cycle_colors[idx])
    print(paste0("Cycle ", idx))
  }
})

legend("topright", legend = legend_labels, col = legend_colors, pch=19, cex = 0.8, title = "H1 Features")
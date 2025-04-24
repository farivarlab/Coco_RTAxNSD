# plot separately
num_graphs <- length(h1_cycles)
cols <- 2  # Arrange in a roughly square grid
rows <- ceiling(num_graphs / cols)
par(mfrow = c(rows, cols), mar = c(1, 1, 1, 1))  # Adjust margins

# Generate distinct colors for different features
feature_colors <- brewer.pal(max(3, num_graphs), "Set3")[1:num_graphs]

image_size <- 0.05

for (i in seq_along(h1_cycles)) {
    cycle_nodes <- h1_cycles[[i]]

    # Skip empty cycles
    if (length(cycle_nodes) == 0) {
        next
    }

    # Convert to character (since VR graph stores them as strings)
    cycle_nodes <- as.character(cycle_nodes)

    # Extract edges that exist between cycle nodes
    all_edges <- full_vr_graph$graphs[[length(full_vr_graph$graphs)]]$graph
    sub_edges <- all_edges[all_edges[,1] %in% cycle_nodes & all_edges[,2] %in% cycle_nodes, , drop = FALSE]

    # Create an igraph object
    g <- graph_from_edgelist(as.matrix(sub_edges), directed = FALSE)
    # Assign colours
    V(g)$color <- feature_colors[i]
    coords <- layout_with_fr(g)
    plot(g,  vertex.size = 25, main = paste("H1 Feature", i), layout=coords)

}
par(mfrow = c(1, 1))
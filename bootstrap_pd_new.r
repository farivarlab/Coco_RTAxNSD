library(reticulate)

use_python("/home/nsd-lab/NSD_cogsci-main/.venv/bin/python", required = TRUE)
source_python("RTA_helpers.py")
np <- import("numpy")
print("loading npy")
rdm <- np$load("data/V1_RDM.npy") #crashes here

# Compute enclosing radius
print("enclosing radius")
cutoff <- enclosing_radius(rdm)
cat("Enclosing radius:", cutoff, "\n")

# Run persistent homology using 90% of enclosing radius
print("persistent homology")
result <- compute_ripser(rdm, scale_factor = 0.9)

# Extract H1
h1_diag <- result$H1
cutoff_used <- result$cutoff

cat("Cutoff used:", cutoff_used, "\n")
cat("H1 features:", length(h1_diag), "\n")

# Save to CSV
write.csv(do.call(rbind, h1_diag), file = "results/V1_H1.csv", row.names = FALSE)

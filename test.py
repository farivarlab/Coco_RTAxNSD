import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.stats import rankdata
import gc

def simulate_and_test_rdm(n_samples=30000, n_features=5000):
    print(f"🚀 Simulating random data: {n_samples} × {n_features} ...")
    
    # Step 1: Generate random data
    matrix = np.random.rand(n_samples, n_features).astype(np.float32)

    # Step 2: Apply Spearman-style rank transform
    print("🔁 Applying row-wise rank transform...")
    ranked = np.empty_like(matrix)
    for i in range(n_samples):
        ranked[i] = rankdata(matrix[i], method="average")
        if i % 1000 == 0:
            print(f"  ...ranked {i}/{n_samples}")

    # Step 3: Compute full correlation distance matrix
    print("📏 Computing full pairwise correlation distance matrix...")
    rdm = pairwise_distances(ranked, metric="correlation").astype(np.float32)

    print("✅ RDM computed:", rdm.shape)

    # Step 4: Save and preview (optional)
    np.save("simulated_RDM_10k.npy", rdm)
    print("💾 Saved to simulated_RDM_30k.npy")

    # Clean up memory
    del matrix, ranked, rdm
    gc.collect()

simulate_and_test_rdm()

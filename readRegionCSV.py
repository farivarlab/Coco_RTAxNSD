import pandas as pd

# Load the table (replace with the actual filename)
df = pd.read_csv("/Users/magico/Desktop/Glasser_2016_Table.csv")  # Modify if needed (e.g., .tsv, .xlsx)

# Convert 'Sections' to string for consistent filtering
df["Sections"] = df["Sections"].astype(str)

# Define region mappings in priority order (first match wins)
region_priority = {
    "Medial_Temporal": "13",
    "Lateral_Temporal": "14",
    "Ventral_Stream_Visual": "4",
    "MT+_Complex_and_Neighboring_Visual_Areas": "5"
}

# Set to track already assigned areas
seen_areas = set()

# Store results
region_results = {}

for region_name, code in region_priority.items():
    # Filter areas belonging to the current region, ensuring uniqueness
    filtered = df[df["Sections"].str.contains(rf"\b{code}\b", regex=True)]
    unique_areas = filtered[~filtered["AreaName"].isin(seen_areas)]
    
    # Update seen areas
    seen_areas.update(unique_areas["AreaName"])

    # Store results
    region_results[region_name] = list(unique_areas["AreaName"])

# Print results
for region, areas in region_results.items():
    print(f"{region}:")
    print(", ".join(f'"{area}"' for area in areas))
    print()

# Print one-line summary of all unique areas
all_unique_areas = [area for areas in region_results.values() for area in areas]
print("Total Summary of " + str(len(all_unique_areas)) + " regions:")
print(", ".join(f'"{area}"' for area in all_unique_areas))
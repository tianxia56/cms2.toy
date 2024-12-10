#!/bin/bash

# List of files to download
files=(
  "gs://fc-97de97ff-f4ee-414a-bf2d-a5f045b20a79/submissions/09af50a3-349e-49b6-a7ac-77600f20fbef/cms2_main/bdc3f68f-c510-4b07-b589-6379dd89e4f7/call-main_call/run_sims_and_compute_cms2_components_wf/3b1fd018-81de-4809-aea0-0c8e9f112c2a/call-component_stats_for_sel_sims_wf/component_stats_for_sel_sims_wf/350901af-b6f1-45c4-8956-d56e5b49120b/call-ScatterAt27_13/shard-0/ScatterAt27_13/03ca4558-3b7a-46f7-883d-28728f481a3f/call-collate_stats_and_metadata_for_sel_sims_block/shard-0/sim.cosi2.model_best_default_112115_825am__demography__selscen_0__selblk_0.all_component_stats.tsv.gz"
  "gs://fc-97de97ff-f4ee-414a-bf2d-a5f045b20a79/submissions/09af50a3-349e-49b6-a7ac-77600f20fbef/cms2_main/bdc3f68f-c510-4b07-b589-6379dd89e4f7/call-main_call/run_sims_and_compute_cms2_components_wf/3b1fd018-81de-4809-aea0-0c8e9f112c2a/call-component_stats_for_sel_sims_wf/component_stats_for_sel_sims_wf/350901af-b6f1-45c4-8956-d56e5b49120b/call-ScatterAt27_13/shard-0/ScatterAt27_13/03ca4558-3b7a-46f7-883d-28728f481a3f/call-collate_stats_and_metadata_for_sel_sims_block/shard-1/sim.cosi2.model_best_default_112115_825am__demography__selscen_0__selblk_1.all_component_stats.tsv.gz"
)

# Directory to save the downloaded files
output_dir="./downloaded_files"
mkdir -p "$output_dir"

# Download and rename files
for file in "${files[@]}"; do
  # Extract the base name of the file
  base_name=$(basename "$file")
  
  # Create a short name by removing everything before "model"
  short_name=$(echo "$base_name" | sed 's/.*model/model/')
  
  # Download the file
  gsutil cp "$file" "$output_dir/$short_name"
done

echo "Files downloaded and renamed successfully."

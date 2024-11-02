library(dplyr)
library(readr)
library(scales)
library(tidyr)

# Create the output directory if it doesn't exist
output_dir <- "normed_scores_take1"
if (!dir.exists(output_dir)) {
  dir.create(output_dir)
}

# Log file for missing files
log_file <- file.path(output_dir, "missing_files.log")
file.create(log_file)

# Function to normalize columns in a DataFrame
normalize_columns <- function(df, columns) {
  if (all(columns %in% colnames(df))) {
    df[columns] <- lapply(df[columns], rescale)
  } else {
    stop("Some columns to normalize are not present in the dataframe")
  }
  return(df)
}

# Randomly select 1000 prefixes from neut-hap.1 to neut-hap.5000
neut_hap_prefixes <- sprintf("neut-hap.%d", 1:5000)
selected_neut_hap_prefixes <- sample(neut_hap_prefixes, 1000)

# Columns to normalize
columns_to_normalize <- c("ihs", "nsl", "ihh12", "xpehh")

# Process hap files in batches of 30 until all are processed
hap_prefixes <- sprintf("hap.%04d", 0:5000)
set.seed(123)  # For reproducibility
hap_prefixes <- sample(hap_prefixes)

for (batch_start in seq(1, length(hap_prefixes), by = 30)) {
  selected_hap_prefixes <- hap_prefixes[batch_start:min(batch_start + 29, length(hap_prefixes))]
  
  # Combine the selected prefixes
  selected_prefixes <- c(selected_hap_prefixes, selected_neut_hap_prefixes)
  
  # Initialize an empty DataFrame to store all data for normalization
  all_data_for_normalization <- data.frame()
  
  # Extract the un-normed scores along with CHR and POS columns, remove NA rows, and concatenate them
  for (prefix in selected_prefixes) {
    if (startsWith(prefix, "neut-hap")) {
      file_path <- file.path("neut.haps", paste0(prefix, "_merged_components.tsv"))
    } else {
      file_path <- paste0(prefix, "_merged_components.tsv")
    }
    
    if (file.exists(file_path)) {
      data <- read_tsv(file_path, show_col_types = FALSE)
      print(paste("Reading file:", file_path))
      if (all(columns_to_normalize %in% colnames(data))) {
        data_subset <- data %>% select(sim.id, pos, all_of(columns_to_normalize)) %>% drop_na()
        print(paste("Rows after removing NA in", file_path, ":", nrow(data_subset)))
        all_data_for_normalization <- bind_rows(all_data_for_normalization, data_subset)
      } else {
        print(paste("Columns not found in", file_path))
      }
    } else {
      print(paste("File not found:", file_path))
      write(paste("File not found:", file_path), file = log_file, append = TRUE)
    }
  }
  
  # Normalize the specified columns across all data
  if (nrow(all_data_for_normalization) > 0) {
    all_data_normalized <- normalize_columns(all_data_for_normalization, columns_to_normalize)
    
    # Rename the normed columns
    all_data_normalized <- all_data_normalized %>% rename_with(~ paste0(., "_normed"), columns_to_normalize)
    
    # Match back to the original TSV by CHR and POS and add normed scores
    for (prefix in selected_hap_prefixes) {
      file_path <- paste0(prefix, "_merged_components.tsv")
      if (file.exists(file_path)) {
        data <- read_tsv(file_path, show_col_types = FALSE)
        normed_data <- left_join(data, all_data_normalized, by = c("sim.id", "pos"))
        
        # Remove the un-normed columns and keep the normed ones
        normed_data <- normed_data %>% select(-all_of(columns_to_normalize))
        
        # Save the new TSV to the designated folder
        normed_file_path <- file.path(output_dir, paste0(prefix, "_normed_components.tsv"))
        write_tsv(normed_data, normed_file_path)
      }
    }
  } else {
    print("No data to normalize in this batch")
  }
}

print("Normalization and saving of files completed successfully.")


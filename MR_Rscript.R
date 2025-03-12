# Pipeline script for batch Mendelian Randomization analysis of exposure-outcome pairs
# Package Dependency Installation: install.packages(c("TwoSampleMR", "MRPRESSO", "ggplot2"))

# Load required libraries
library(TwoSampleMR)  # Library for Mendelian Randomization analysis
library(MRPRESSO)     # Library for MR-PRESSO outlier detection
library(ggplot2)      # Library for creating plots

# ---------------------------------------------------------------------
# Step 1: Read the list of file paths
# ---------------------------------------------------------------------

# Read the file containing paths to exposure and outcome data
file_list <- read.table(file_path, header = TRUE, stringsAsFactors = FALSE)

# ---------------------------------------------------------------------
# Step 2: Define the analysis function
# ---------------------------------------------------------------------
run_mr_analysis <- function(exposure_path, outcome_path, output_prefix) {

  # Read exposure data 
  exposure_dat <- read.table(exposure_path,header=T)
  
  # Read outcome data
  outcome_dat <- read.table(outcome_path,header=T)
  
  # Align the data
  dat <- harmonise_data(exposure_dat, outcome_dat)
  
  # Perform the MR analysis
  res <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression","mr_weighted_median","mr_two_sample_ml","mr_raps"))
  
  # Perform MR-PRESSO outlier detection
  presso <- run_mr_presso(dat, NbDistribution = 1000) 
  # Convert beta values to odds ratios
  res_or<-generate_odds_ratios(res)


  # Perform heterogeneity test to assess variability in MR results
  het <- mr_heterogeneity(dat)  # Heterogeneous results were obtained
  
  # Merge MR results with heterogeneity test results
  res_with_het <- merge( res_or,het[, c("method", "Q", "Q_pval")],  # Extract key columns by = "method", 
    all.x = TRUE
  )
  
# Perform horizontal pleiotropy test (Egger intercept)
  pleiotropy <- mr_pleiotropy_test(dat) %>% rename(egger_se = se,egger_pval = pval)
  pleiotropy$method="MR Egger"

  # Merge MR results with pleiotropy test results
  new_res_with_het <- merge(res_with_het,pleiotropy[, c("method", "egger_intercept", "egger_se","egger_pval")],  by = "method", all.x = TRUE)

  # Extract significant results with p-value < 0.05
  sig_res <- res_or %>% filter(res_or$pval < 0.05)
  
  # If significant results are found, save plots and append results  
  if (nrow(sig_res) > 0) {
    all_results <- rbind(all_results, sig_res)
    
    # Save scatter plot
    scatter_plot <- mr_scatter_plot(res, dat)
    ggsave(paste0("scatter_plot_", i, ".pdf"), scatter_plot[[1]], width = 8, height = 6)
    
    # Save forest plot
    forest_plot <- mr_forest_plot(res)
    ggsave(paste0("forest_plot_", i, ".pdf"), forest_plot[[1]], width = 8, height = 6)
    
    # Save funnel plot
    funnel_plot <- mr_funnel_plot(res)
    ggsave(paste0("funnel_plot_", i, ".pdf"), funnel_plot[[1]], width = 8, height = 6)
    
    # Save leave-one-out plot
    result_loo <- mr_leaveoneout(dat)
    leaveoneout_plot <- mr_leaveoneout_plot(result_loo)
    ggsave(paste0("leaveoneout_plot_", i, ".pdf"), leaveoneout_plot[[1]], width = 8, height = 6)
    
  }

  # Return analysis results and MR-PRESSO results
  return(list(results = new_res_with_het, presso = presso))
}

# ---------------------------------------------------------------------
# Step 3: Execute the batch analysis
# ---------------------------------------------------------------------

# Initialize a list to store all analysis results
all_results <- list()

# Loop through each file pair in the file list
for(i in 1:nrow(file_list)) {
  exp_path <- file_list$exposure_path[i]  # Path to exposure data
  out_path <- file_list$outcome_path[i]   # Path to outcome data
  
  # Check if exposure file exists; if not, skip and issue a warning  
  if(!file.exists(exp_path)) {
    warning(paste("exposure_file not found:", exp_path))
    next
  }

  # Check if outcome file exists; if not, skip and issue a warning
  if(!file.exists(out_path)) {
    warning(paste("outcome_file not found:", out_path))
    next
  }
  
  # Define output name for the current analysis
  output_name <- paste0("MR_Result_", i)

    # Attempt to run MR analysis; catch and report any errors
    tryCatch({
      all_results[[i]] <- run_mr_analysis(exp_path, out_path, output_name)
    }, error = function(e) {
      message(paste("Analysis failed:", e$message))
    })
}

# ---------------------------------------------------------------------
# Step 4: Summarize the analysis results
# ---------------------------------------------------------------------

# Merge all results into a single data frame
final_res <- do.call(rbind, lapply(all_results, function(x) x$results))

# Save the summary results to a CSV file
write.csv(final_res, result_file, row.names = FALSE)

## Generate a summary report and save it to a text file
sink("analysis_report.txt")
cat("Mendelian randomization analysis summary report\n")
cat("==========================\n\n")
cat(paste("Analysis time:", Sys.time(), "\n"))
cat(paste("Total analysis pairs:", nrow(file_list), "\n"))
cat(paste("Successful analyses:", sum(sapply(all_results, function(x) !is.null(x))), "\n\n"))

# Print the final results to the report
print(final_res)
sink()














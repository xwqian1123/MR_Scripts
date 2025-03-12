# Pipeline script for batch Mendelian Randomization analysis of exposure-outcome pairs

# Install required R packages
install.packages(c("TwoSampleMR", "MRPRESSO", "ggplot2", "dplyr"))

# Load essential libraries
library(TwoSampleMR)  # Load TwoSampleMR package for MR analysis
library(MRPRESSO)     # Load MRPRESSO package for outlier detection
library(ggplot2)      # Load ggplot2 for visualization 
library(dplyr)

# ---------------------------------------------------------------------
# Step 1: Read file path list
# ---------------------------------------------------------------------

# Get input file path from command line argument
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("Error: Please provide the input file path as a command line argument")
}
inputfile_path <- args[1]

# Read the file containing exposure-outcome pairs' paths
file_list <- read.table(inputfile_path, header = TRUE, stringsAsFactors = FALSE)

# ---------------------------------------------------------------------
# Step 2: Define the MR analysis function
# ---------------------------------------------------------------------
run_mr_analysis <- function(exposure_path, outcome_path, output_prefix) {

  # Read exposure data
  exposure_dat <- read.table(exposure_path,header=T)
  
  # Read outcome data
  outcome_dat <- read.table(outcome_path,header=T)
  
  # Align the data
  dat <- harmonise_data(exposure_dat, outcome_dat)
  
  # Perform the MR analysis
  res <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression", 
                                 "mr_weighted_median","mr_two_sample_ml","mr_raps"))
  
  # Detect outlier SNPs using MR-PRESSO method
  presso <- run_mr_presso(dat, NbDistribution = 1000)  # Note: computationally intensive
  
  # Convert beta coefficients to odds ratios
  res_or<-generate_odds_ratios(res)
  
  # Perform heterogeneity test to assess result variability
  het <- mr_heterogeneity(dat)  
  
  # Merge MR results with heterogeneity statistics
  res_with_het <- merge(
    res_or, 
    het[, c("method", "Q", "Q_pval")],  # Extract key columns
    by = "method", 
    all.x = TRUE
  )
  
  # Perform horizontal pleiotropy test (MR-Egger regression)
  pleiotropy <- mr_pleiotropy_test(dat) %>%
    rename(
      egger_se = se,
      egger_pval = pval
    )
  pleiotropy$method="MR Egger"

  # Combine results with pleiotropy test
  new_res_with_het <- merge(
    res_with_het, 
    pleiotropy[, c("method", "egger_intercept", "egger_se","egger_pval")],  # 提取关键列
    by = "method", 
    all.x = TRUE
  )
  
  # Extract statistically significant results (p < 0.05)
  sig_res <- res_or %>% filter(res_or$pval < 0.05)

  if (nrow(sig_res) > 0) {
    # Save scatter plot (SNP effect sizes)
    scatter_plot <- mr_scatter_plot(res, dat)
    ggsave(paste0(output_prefix, i, "_scatter.pdf"), scatter_plot[[1]], width = 8, height = 6)
    
    # Save forest plot (individual SNP contributions)
    result_single <- mr_singlesnp(dat)
    forest_plot <- mr_forest_plot(result_single)
    ggsave(paste0(output_prefix, i, "_forest.pdf"), forest_plot[[1]], width = 8, height = 6)

    # Save funnel plot (publication bias assessment)
    funnel_plot <- mr_funnel_plot(result_single)
    ggsave(paste0(output_prefix, i, "_funnel.pdf"), funnel_plot[[1]], width = 8, height = 6)
    
    # Save leave-one-out analysis plot
    result_loo <- mr_leaveoneout(dat)
    leaveoneout_plot <- mr_leaveoneout_plot(result_loo)
    ggsave(paste0(output_prefix, i, "_leaveoneout.pdf"), leaveoneout_plot[[1]], width = 8, height = 6)
    
  }

  # Return analysis results and outlier detection output
  return(list(results = new_res_with_het, presso = presso))
}

# ---------------------------------------------------------------------
# Step 3: Execute batch analysis
# ---------------------------------------------------------------------

# Initialize results storage
all_results <- list()

# Iterate through each exposure-outcome pair
for(i in 1:nrow(file_list)) {
  exp_path <- file_list$exposure_path[i]  # Get exposure data path
  out_path <- file_list$outcome_path[i]   # Get outcome data path
  
  # Check file existence before processing
  if(!file.exists(exp_path)) {
    warning(paste("Exposure file not found:", exp_path))
    next  # Skip to next iteration if file missing
  }
  if(!file.exists(out_path)) {
    warning(paste("Outcome file not found:", out_path))
    next
  }
  
  # Generate output prefix
  output_name <- paste0("MR_Result_", i)
    tryCatch({
      all_results[[i]] <- run_mr_analysis(exp_path, out_path, output_name)
    }, error = function(e) {
      message(paste("Analysis failed:", e$message))
    })
}

# ---------------------------------------------------------------------
# Step 4: Summarize results
# ---------------------------------------------------------------------

# Combine all results into single dataframe
final_res <- do.call(rbind, lapply(all_results, function(x) x$results))

# Save combined results to CSV
write.csv(final_res, "combined_mr_results3.csv", row.names = FALSE)

# Generate summary report
sink("analysis_report.txt")
cat("Mendelian Randomization Analysis Summary Report\n")
cat("==========================\n\n")
cat(paste("Analysis time:", Sys.time(), "\n"))
cat(paste("Total analysis pairs:", nrow(file_list), "\n"))
cat(paste("Successful analyses:", sum(sapply(all_results, function(x) !is.null(x))), "\n\n"))

# Print final results to report
print(final_res)
# Close output redirection
sink()

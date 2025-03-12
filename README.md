# Mendelian Randomization Analysis Scripts  
This repository provides reproducible scripts and tools for Mendelian Randomization (MR) analysis. It supports functions such as causal effect inference, heterogeneity testing, and sensitivity analysis.

## Project Description
Mendelian Randomization is a method that uses genetic variants as instrumental variables (IVs) to evaluate the causal relationship between exposure factors (e.g., gene expression, metabolites) and disease outcomes. This repository includes:
- Core analysis scripts based on the R language.
- Data preprocessing tools.
- Visualization functions.
- Sensitivity analysis modules (e.g., MR-Egger, weighted median, Leave-one-out).

## Usage Instructions
### Input Data Requirements
1. Exposure data:
   - It should contain SNP names, effect alleles, other alleles, effect sizes, and standard errors.
2. Outcome data:
   - The format is the same as the exposure data.
3. Covariate data (optional): Information on confounding factors.

### Run the Script
```r
# Load custom functions
source("scripts/mr_analysis.R")

# Perform the core analysis
result <- run_mr_analysis(
  exposure_data = "data/exposure.csv",
  outcome_data = "data/outcome.csv",
  covariates = "data/covariates.csv"
)

# Generate the result report
generate_report(result, output_dir = "results/")
```

## Example Analysis Workflow
1. **Data Preparation**: Organize the GWAS summary data into the specified format.
2. **Instrumental Variable Selection**: Filter SNPs based on the F-statistic and p-value.
3. **Causal Effect Estimation**:
   - Inverse Variance Weighted (IVW).
   - Weighted Median.
   - MR-Egger Regression.
4. **Heterogeneity Testing**:
   - Cochran's Q test.
   - Leave-one-out method.
5. **Visualization**:
   - Forest plot.
   - Funnel plot.
   - Scatter plot of causal effects.







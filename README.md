# Mendelian Randomization Analysis Scripts  
This repository provides reproducible scripts and tools for Mendelian Randomization (MR) analysis. It supports functions such as causal effect inference, heterogeneity testing, and sensitivity analysis.

![IMAGE](https://github.com/xwqian1123/MR_Scripts/blob/main/img/mr.png)

> [!IMPORTANT]
> The development of these scripts aims to promote the widespread application of MR analysis in the field of genetic epidemiology and related disciplines. We hope that by providing easy - to - use and reliable tools, more researchers can uncover causal relationships between genetic factors and complex diseases, ultimately contributing to the advancement of precision medicine and disease prevention strategies.

## 📚 Table of Contents
- [⚡ Project Description](#project-description)
- [🛠️ Installation Guide](#installation-guide)
- [💡 Usage Instructions](#usage-instructions)
- [🤖 Example Analysis Workflow](#example-analysis-workflow)

## ⚡ Project Description
Mendelian Randomization is a method that uses genetic variants as instrumental variables (IVs) to evaluate the causal relationship between exposure factors (e.g., gene expression, metabolites) and disease outcomes. This repository includes:
- Core analysis scripts based on the R language.
- Data preprocessing tools.
- Visualization functions.
- Sensitivity analysis modules (e.g., MR-Egger, weighted median, Leave-one-out).

## 🛠️ Installation Guide
### Dependencies
1. Install the R language environment (version ≥ 4.3 is recommended).
2. Install R packages:
```r
install.packages(c("TwoSampleMR", "MRPRESSO", "ggplot2", "dplyr"))   
```

### Get the Code
```bash
git clone https://github.com/xwqian1123/MR_Scripts.git
cd MR_Scripts
```

## 💡 Usage Instructions
### Input Data Requirements
1. Exposure data:
   - It should contain SNP names, effect alleles, other alleles, effect sizes, and standard errors.
2. Outcome data:
   - The format is the same as the exposure data.
3. Covariate data (optional): Information on confounding factors.

### Run the Scripts
```shell
step1.  cd MibioGen; 
Step2.  ls *.summary.txt | perl -ne 'chomp;print "sed -i '\''1s/rsID/SNP/'\'' $_\n"' > rename.sh
	sh rename.sh
	ls *.summary.txt | perl -ne 'chomp;print "sed -i '\''1s/P.weightedSumZ/P/'\'' $_\n"' > rename.sh
	sh rename.sh
	ls *.summary.txt > list_path.txt
	python3 filtered_dat.py

Step3.	ls *_filtered.txt | perl -ne 'chomp;@t=split(/\./,$_);print "/root/software/plink --bfile EDU/EUR --clump $_ --clump-p1 1 --clump-r2 0.001 --clump-kb 10000 -out clump_$t[1].$t[2].$t[3]\n";' > plink.sh
	sh plink.sh
	ls *.clumped | perl -ne 'chomp;print" python3 retype.py $_\n";' > retype.sh
	sh retype.sh

Step4	ls *.summary.txt | perl -ne'chomp;@t=split(/\.summary.txt/,$_);@p=split(/\./,$t[0]);print "python3 get_bac.py out_clump_$p[0].$p[1].$p[3].clump $t[0].summary_filtered.txt\n";' > get_bac.sh
	sh get_bac.sh

Step5	ls mer_out.*|perl -ne'chomp;@at=split(/\mer_out./);print"python3 all_ex_out.py $_ finnger_R11_O15_PREECLAMPS\n";'>all_ex_out.sh
	sh all_ex_out.sh

Step6   ls R11_* | perl -ne 'chomp;@t=split(/\_/,$_);@p=split(/\./,$t[4]);print "python3 get_result.py $_ R11_$p[0].$p[1].$p[2]\n";' > result.sh
	sh result.sh
	ls *.exposure.txt | perl -ne 'chomp;@t=split(/\./,$_);print"$_\t$t[0].$t[1].$t[2].outcome.txt\n";' > file_path.txt
Step7	Rscript mr_analysis.R file_path.txt
```

## 🤖 Example Analysis Workflow
1. **Data Preparation**: Organize the GWAS summary data into the specified format.
2. **Instrumental Variable Selection**: Filter SNPs based on the p-value.
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







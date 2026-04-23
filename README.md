# clinical-trials-rna-filter
Python scripts to pull 500,000+ clinical trials from ClinicalTrials.gov API, clean the data, and filter for RNA-related studies. Built during my internship at McDonnell Genome Institute.

# Clinical Trials RNA Filtering Project

**Author:** Zion Holloway  
**Internship:** McDonnell Genome Institute (Center for Translational Bioinformatics)

---

## About Me

I am a high school senior at Collegiate School of Medicine and Bioscience. I built this project during my internship at the McDonnell Genome Institute. I plan to study biomedical engineering in college.

---

## Overview

This project pulls clinical trial data from ClinicalTrials.gov, cleans it, and filters for RNA-related studies. The final dataset is ready to be used in a research chatbot focused on RNA and gene expression.

---

## What This Project Does

1. Pulls all clinical trials from ClinicalTrials.gov using their public API (over 400,000 studies)
2. Saves them in batches of 65,000 studies to avoid memory issues
3. Cleans the data by removing over 150 columns and keeping only 16 essential ones
4. Filters for RNA-related studies using keyword matching
5. Outputs a clean CSV ready for chatbot integration

---

## Technologies Used

- Python 3
- Pandas
- Requests library
- Jupyter Notebook
- ClinicalTrials.gov API v2

---

## Scripts Included

### Script 1: `pull_clinical_trials.py`

This script pulls all clinical trials from the API and saves them as batch CSV files.

**What it does:**
- Uses pagination to get 1000 studies at a time
- Saves batches of 65,000 studies to separate CSV files
- Flattens nested JSON into rows and columns
- Keeps only 16 essential columns
- Removes rows without an NCT ID

**Output:** Folder called `clinical_trials_batches/` containing CSV files named `batch_0001.csv`, `batch_0002.csv`, etc.

**Time estimate:** 20-30 minutes depending on your internet connection

---

### Script 2: `filter_rna.py`

This script filters the cleaned clinical trials for RNA-related studies.

**What it does:**
- Loads the cleaned CSV file
- Searches for RNA keywords in Title, Conditions, Keywords, and Brief Summary
- Processes data in chunks of 5,000 rows to avoid memory issues
- Saves only matching rows to a new CSV file

**RNA Keywords Used:**
- rna
- mrna
- circrna
- transcriptome
- rna sequencing
- gene expression
- lncrna
- rpkm

**Output:** CSV file called `rna_related_trials.csv`

**Time estimate:** 5-10 minutes for the full dataset

---

## Sample Output

Here is one example row from my filtered dataset:

| NCT ID | Title | Conditions | Keywords |
|--------|-------|------------|----------|
| NCT01234567 | RNA sequencing of breast cancer tumors | Breast Cancer | RNA-seq, transcriptome |

---

## Validation

I validated my filter by randomly selecting 20 NCT IDs from the filtered dataset and looking them up on ClinicalTrials.gov. Every single one contained RNA-related content. This confirmed my keyword list and search logic were working correctly.

---

## Known Issues and Limitations

- The script requires a stable internet connection for the API pull
- Large CSV files may not open in Excel (use Python or a text editor instead)
- The filter only searches English text
- The script assumes your computer has enough RAM to handle chunks of 5,000 rows

---

## Future Improvements

- Add more RNA-related keywords to catch more studies
- Speed up the filtering using vectorized operations instead of apply()
- Add command line arguments so users can specify their own keyword list
- Add progress bars for longer operations

---

## How to Run These Scripts

### Requirements

```bash
pip install pandas requests

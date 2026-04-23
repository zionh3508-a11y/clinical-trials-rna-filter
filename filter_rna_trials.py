import pandas as pd

input_file = "clinical_trials_cleaned_full.csv"
output_file = "rna_related_trials#2.csv"

# RNA-related keywords
keywords = [
    "rna",
    "mrna",
    "circrna",
    "transcriptome",
    "rna sequencing",
    "gene expression",
    "lncrna",
    "rpkm"
]

chunksize = 5000

print("Starting RNA filtering...")
print(f"Reading from: {input_file}")

first_chunk = True
total_filtered = 0

for chunk in pd.read_csv(
    input_file,
    chunksize=chunksize,
    low_memory=False
):

    # Convert text to lowercase
    text_data = chunk.astype(str).apply(lambda x: x.str.lower())

    mask = text_data.apply(
        lambda row: any(keyword in row.to_string() for keyword in keywords),
        axis=1
    )

    filtered = chunk[mask]
    total_filtered += len(filtered)

    if not filtered.empty:
        filtered.to_csv(
            output_file,
            mode='a',
            header=first_chunk,
            index=False
        )
        first_chunk = False
        print(f"Found {len(filtered)} RNA-related studies in this chunk")

print(f"\nDone. Total RNA-related studies found: {total_filtered}")
print(f"Saved to: {output_file}")
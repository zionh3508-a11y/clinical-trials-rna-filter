import requests
import json
import pandas as pd
import os

os.chdir("/home/zion")

# Create a folder for batches
batch_folder = "clinical_trials_batches"
if not os.path.exists(batch_folder):
    os.makedirs(batch_folder)

# Step 1: API setup

base_url = "https://clinicaltrials.gov/api/v2/studies"

all_studies = []
page_token = None
page_count = 0
batch_size = 65000  # Save to file every 65,000 studies
batch_number = 1

# Step 2: Pull ALL data and save in batches

print("Starting to pull all studies. This will take a while...")

while True:
    params = {
        "format": "json",
        "pageSize": 1000
    }

    if page_token:
        params["pageToken"] = page_token

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        break

    data = response.json()
    studies = data.get("studies", [])
    all_studies.extend(studies)

    page_count += 1
    print(f"Page {page_count}: pulled {len(studies)} studies (total in memory: {len(all_studies)})")

    # Check if we've reached batch size
    if len(all_studies) >= batch_size:
        # Flatten current batch
        print(f"  Reached {len(all_studies)} studies. Saving batch {batch_number}...")
        df = pd.json_normalize(all_studies)
        
        # Keep only essential columns
        essential_columns = {
            'protocolSection.identificationModule.nctId': 'NCT ID',
            'protocolSection.identificationModule.briefTitle': 'Title',
            'protocolSection.statusModule.overallStatus': 'Status',
            'protocolSection.statusModule.startDateStruct.date': 'Start Date',
            'protocolSection.statusModule.completionDateStruct.date': 'Completion Date',
            'protocolSection.designModule.phase': 'Phase',
            'protocolSection.designModule.studyType': 'Study Type',
            'protocolSection.designModule.enrollmentInfo.count': 'Enrollment Count',
            'protocolSection.conditionsModule.conditions': 'Conditions',
            'protocolSection.conditionsModule.keywords': 'Keywords',
            'protocolSection.armsInterventionsModule.interventions': 'Interventions',
            'protocolSection.eligibilityModule.eligibilityCriteria': 'Eligibility Criteria',
            'protocolSection.eligibilityModule.gender': 'Gender',
            'protocolSection.eligibilityModule.minimumAge': 'Minimum Age',
            'protocolSection.eligibilityModule.maximumAge': 'Maximum Age',
            'protocolSection.outcomesModule.primaryOutcomes': 'Primary Outcomes',
            'protocolSection.outcomesModule.secondaryOutcomes': 'Secondary Outcomes',
            'protocolSection.contactsLocationModule.locations': 'Locations',
            'protocolSection.descriptionModule.briefSummary': 'Brief Summary',
            'derivedSection.conditionBrowseModule.conditions': 'Condition Browse',
        }
        
        keep_cols = [col for col in essential_columns.keys() if col in df.columns]
        df = df[keep_cols]
        df = df.rename(columns=essential_columns)
        
        # Remove rows without NCT ID
        df = df.dropna(subset=['NCT ID'], how='all')
        
        # Save batch
        batch_filename = f"{batch_folder}/batch_{batch_number:04d}.csv"
        df.to_csv(batch_filename, index=False, encoding='utf-8')
        print(f"  Saved {len(df)} studies to {batch_filename}")
        
        # Clear memory for next batch
        all_studies = []
        batch_number += 1

    page_token = data.get("nextPageToken")

    if not page_token:
        print("No more pages. Saving final batch...")
        # Save remaining studies
        if len(all_studies) > 0:
            df = pd.json_normalize(all_studies)
            keep_cols = [col for col in essential_columns.keys() if col in df.columns]
            df = df[keep_cols]
            df = df.rename(columns=essential_columns)
            df = df.dropna(subset=['NCT ID'], how='all')
            batch_filename = f"{batch_folder}/batch_{batch_number:04d}.csv"
            df.to_csv(batch_filename, index=False, encoding='utf-8')
            print(f"  Saved final batch {batch_number} with {len(df)} studies")
        break

print(f"\nAll batches saved in folder: {batch_folder}")
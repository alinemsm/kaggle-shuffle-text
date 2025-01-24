import os
import logging
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from collections import Counter

def setup_kaggle_api() -> KaggleApi:
    """Initialize and authenticate Kaggle API"""
    try:
        api = KaggleApi()
        api.authenticate()
        return api
    except Exception as e:
        logging.error(f"Failed to authenticate with Kaggle API: {str(e)}")
        raise

def submit_to_kaggle(submission_file: str, message: str, competition_name: str) -> bool:
    """
    Submit a solution to a Kaggle competition
    
    Args:
        submission_file (str): Path to the submission file
        message (str): Submission message
        competition_name (str): Name of the Kaggle competition
    
    Returns:
        bool: True if submission was successful, False otherwise
    """
    if not os.path.exists(submission_file):
        logging.error(f"Submission file not found: {submission_file}")
        return False
    
    try:
        api = setup_kaggle_api()
        
        # Make submission
        api.competition_submit(
            file_name=submission_file,
            message=message,
            competition=competition_name
        )
        logging.info(f"Successfully submitted {submission_file}")
        return True
        
    except Exception as e:
        logging.error(f"Submission failed: {str(e)}")
        return False 

def verify_submission_integrity(original_file: str, submission_file: str) -> bool:
    """
    Verify that the submission file contains exactly the same words as the original,
    comparing each row separately.
    
    Args:
        original_file (str): Path to the original sample submission file
        submission_file (str): Path to the new submission file
    
    Returns:
        bool: True if the files contain the same words, False otherwise
    """
    try:
        # Read both files
        original_df = pd.read_csv(original_file)
        submission_df = pd.read_csv(submission_file)
        
        # Verify the dataframes have the same number of rows
        if len(original_df) != len(submission_df):
            logging.error(f"Row count mismatch: original={len(original_df)}, submission={len(submission_df)}")
            return False
        
        all_rows_match = True
        differences = []
        
        # Compare each row
        for idx in range(len(original_df)):
            orig_text = str(original_df.iloc[idx]['text'])
            subm_text = str(submission_df.iloc[idx]['text'])
            
            # Convert texts to word frequency counters
            orig_counts = Counter(orig_text.split())
            subm_counts = Counter(subm_text.split())
            
            if orig_counts != subm_counts:
                all_rows_match = False
                # Find differences for this row
                added = set(subm_counts.keys()) - set(orig_counts.keys())
                removed = set(orig_counts.keys()) - set(subm_counts.keys())
                different_counts = {
                    word: (orig_counts[word], subm_counts[word])
                    for word in set(orig_counts) & set(subm_counts)
                    if orig_counts[word] != subm_counts[word]
                }
                
                differences.append({
                    'row': idx,
                    'original': orig_text,
                    'submission': subm_text,
                    'added': added,
                    'removed': removed,
                    'different_counts': different_counts
                })
        
        if all_rows_match:
            logging.info("All rows verified: Contents match exactly")
            return True
        else:
            logging.error(f"Found differences in {len(differences)} rows")
            for diff in differences:
                logging.error(f"\nRow {diff['row']}:")
                logging.error(f"Original:   {diff['original']}")
                logging.error(f"Submission: {diff['submission']}")
                if diff['added']:
                    logging.error(f"Added words: {diff['added']}")
                if diff['removed']:
                    logging.error(f"Removed words: {diff['removed']}")
                if diff['different_counts']:
                    logging.error("Word count differences:")
                    for word, (orig_count, subm_count) in diff['different_counts'].items():
                        logging.error(f"  '{word}': original={orig_count}, submission={subm_count}")
            return False
            
    except Exception as e:
        logging.error(f"Error comparing submissions: {str(e)}")
        return False 
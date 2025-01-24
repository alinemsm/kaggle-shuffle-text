import pandas as pd
from datetime import datetime

def sort_submission_texts(input_file: str):
    """
    Read sample submission, sort words in each text, and save to new CSV
    """
    # Read the input CSV
    df = pd.read_csv(input_file)
    
    # Process each row
    for idx in range(len(df)):
        # Get original text and split into words
        original_text = str(df.loc[idx, "text"])
        original_count = len(original_text.split())
        
        # Sort words and join back to text
        sorted_text = " ".join(sorted(original_text.split()))
        
        # Verify word count
        final_count = len(sorted_text.split())
        if final_count != original_count:
            print(f"WARNING: Row {idx} word count mismatch! Original: {original_count}, Final: {final_count}")
        
        # Update the dataframe
        df.loc[idx, "text"] = sorted_text
        
        # Progress indicator
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(df)} texts")
    
    # Save to new CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'submission_sorted_{timestamp}.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSorted submission saved to {output_file}")

if __name__ == "__main__":
    input_file = "sample_submission.csv"
    sort_submission_texts(input_file) 
"""
========================================
DATA PROCESSOR MODULE
========================================
This module handles loading, cleaning, and preparing customer insight data
for analysis and classification.

What this module does:
1. Loads data from Excel (.xlsx) or CSV files
2. Cleans and normalizes the text
3. Removes duplicate insights from the same company
4. Prepares data for classification

Key Concepts for Beginners:
- A "DataFrame" is like an Excel spreadsheet in Python (from pandas library)
- "Cleaning" means removing unwanted characters and standardizing format
- "Deduplication" means removing duplicate entries
"""

import pandas as pd
import re
from typing import Optional
import os


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load customer insight data from an Excel or CSV file.
    
    What it does:
    - Reads the file based on its extension (.xlsx, .xls, or .csv)
    - Returns a DataFrame (like a spreadsheet) with all the data
    
    Parameters:
        file_path: The path to your data file (e.g., "data/insights.xlsx")
    
    Returns:
        A pandas DataFrame containing all your data
    
    Example:
        df = load_data("customer_insights.xlsx")
        print(df.head())  # Shows first 5 rows
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find file: {file_path}")
    
    # Determine file type and load accordingly
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension in ['xlsx', 'xls']:
        # Load Excel file
        print(f"📊 Loading Excel file: {file_path}")
        df = pd.read_excel(file_path)
    elif file_extension == 'csv':
        # Load CSV file
        print(f"📄 Loading CSV file: {file_path}")
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: .{file_extension}. Use .xlsx, .xls, or .csv")
    
    print(f"✅ Loaded {len(df)} rows of data")
    return df


def clean_text(text: str) -> str:
    """
    Clean and normalize a single piece of text.
    
    What it does:
    - Removes extra whitespace (spaces, tabs, newlines)
    - Converts to lowercase for consistent matching
    - Removes special characters that might cause issues
    - Keeps the essential content readable
    
    Parameters:
        text: The raw text to clean
    
    Returns:
        The cleaned text
    
    Example:
        clean_text("  Hello   World!!  ")  →  "hello world"
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Convert to string (in case it's a number or other type)
    text = str(text)
    
    # Remove HTML tags if present (e.g., from email imports)
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Replace multiple whitespace characters with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Convert to lowercase for consistent matching
    # We keep a copy of the original for display purposes
    return text


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison and deduplication.
    
    This creates a "fingerprint" of the text that helps us identify duplicates
    even if they have minor differences.
    
    Parameters:
        text: The text to normalize
    
    Returns:
        Normalized text suitable for comparison
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Clean the text first
    text = clean_text(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation (but keep spaces between words)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def clean_company_name(company_name: str) -> str:
    """
    Clean and standardize company names.
    
    This helps identify the same company even with slight name variations.
    
    Parameters:
        company_name: The raw company name
    
    Returns:
        Cleaned company name
    
    Example:
        clean_company_name("Acme Corp.  ")  →  "Acme Corp"
    """
    if pd.isna(company_name) or company_name is None:
        return "Unknown Company"
    
    # Convert to string and strip whitespace
    name = str(company_name).strip()
    
    # Remove common suffixes for better matching (but keep in display)
    # We don't actually remove them, just clean up
    
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name)
    
    # Return empty as "Unknown Company"
    if not name:
        return "Unknown Company"
    
    return name


def remove_duplicates(df: pd.DataFrame, 
                     text_column: str = 'note_text',
                     company_column: str = 'company_name') -> pd.DataFrame:
    """
    Remove duplicate insights from the same company.
    
    What it does:
    - Creates a normalized version of each insight
    - Identifies duplicates where both the text AND company match
    - Keeps the first occurrence, removes later duplicates
    
    Parameters:
        df: The DataFrame with insights
        text_column: Name of the column containing insight text
        company_column: Name of the column containing company names
    
    Returns:
        DataFrame with duplicates removed
    """
    original_count = len(df)
    
    # Create a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Create normalized versions for comparison
    df_clean['_normalized_text'] = df_clean[text_column].apply(normalize_text)
    df_clean['_normalized_company'] = df_clean[company_column].apply(clean_company_name)
    
    # Remove rows where normalized text is empty or just "unknown feedback"
    df_clean = df_clean[df_clean['_normalized_text'] != '']
    df_clean = df_clean[df_clean['_normalized_text'] != 'unknown feedback']
    
    # Remove duplicates based on normalized text + company
    df_clean = df_clean.drop_duplicates(
        subset=['_normalized_text', '_normalized_company'],
        keep='first'
    )
    
    # Remove helper columns
    df_clean = df_clean.drop(columns=['_normalized_text', '_normalized_company'])
    
    removed_count = original_count - len(df_clean)
    print(f"🧹 Removed {removed_count} duplicate/empty insights")
    print(f"📋 Remaining insights: {len(df_clean)}")
    
    return df_clean.reset_index(drop=True)


def prepare_insights(df: pd.DataFrame,
                    text_column: str = 'note_text',
                    company_column: str = 'company_name') -> pd.DataFrame:
    """
    Main function to prepare insights data for classification.
    
    This is the function you'll typically call - it does everything:
    1. Cleans the insight text
    2. Cleans company names
    3. Removes duplicates
    4. Adds helpful columns
    
    Parameters:
        df: Raw DataFrame loaded from file
        text_column: Name of column with insight text
        company_column: Name of column with company names
    
    Returns:
        Clean, deduplicated DataFrame ready for classification
    
    Example:
        raw_df = load_data("insights.xlsx")
        clean_df = prepare_insights(raw_df)
    """
    print("\n🔄 Preparing insights data...")
    
    # Check required columns exist
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found. Available columns: {list(df.columns)}")
    if company_column not in df.columns:
        raise ValueError(f"Column '{company_column}' not found. Available columns: {list(df.columns)}")
    
    # Create a copy
    df_prepared = df.copy()
    
    # Clean the text column (create both cleaned and original versions)
    print("  📝 Cleaning insight text...")
    df_prepared['cleaned_text'] = df_prepared[text_column].apply(clean_text)
    
    # Clean company names
    print("  🏢 Standardizing company names...")
    df_prepared['cleaned_company'] = df_prepared[company_column].apply(clean_company_name)
    
    # Remove duplicates
    print("  🔍 Removing duplicates...")
    df_prepared = remove_duplicates(
        df_prepared, 
        text_column='cleaned_text',
        company_column='cleaned_company'
    )
    
    # Add a unique ID for each insight
    df_prepared['insight_id'] = range(1, len(df_prepared) + 1)
    
    # Add text length (useful for filtering very short/long insights)
    df_prepared['text_length'] = df_prepared['cleaned_text'].str.len()
    
    print(f"\n✅ Data preparation complete!")
    print(f"   Total valid insights: {len(df_prepared)}")
    print(f"   Unique companies: {df_prepared['cleaned_company'].nunique()}")
    
    return df_prepared


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get a summary of the prepared data.
    
    Parameters:
        df: Prepared DataFrame
    
    Returns:
        Dictionary with summary statistics
    """
    return {
        'total_insights': len(df),
        'unique_companies': df['cleaned_company'].nunique(),
        'avg_text_length': df['text_length'].mean() if 'text_length' in df.columns else 0,
        'top_companies': df['cleaned_company'].value_counts().head(10).to_dict(),
    }


# ============================================================================
# QUICK TEST
# ============================================================================
# This code runs only when you run this file directly (not when imported)

if __name__ == "__main__":
    # Test the module with sample data
    print("=" * 50)
    print("Testing Data Processor Module")
    print("=" * 50)
    
    # Test text cleaning
    test_text = "  This is a   TEST   with extra   spaces!  "
    print(f"\nOriginal: '{test_text}'")
    print(f"Cleaned:  '{clean_text(test_text)}'")
    
    # Test company name cleaning
    test_company = "  Acme Corp   "
    print(f"\nOriginal company: '{test_company}'")
    print(f"Cleaned company:  '{clean_company_name(test_company)}'")

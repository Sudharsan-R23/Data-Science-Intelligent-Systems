"""
PDF Data Extraction Script
Extracts tables and text from the uploaded PDF dataset
"""
import pdfplumber
import pandas as pd
import os
from pathlib import Path

def extract_pdf_data(pdf_path):
    """
    Extract data from PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dataframes extracted from the PDF
    """
    print(f"Extracting data from: {pdf_path}")
    
    dataframes = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            
            # Extract tables from each page
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n--- Page {page_num} ---")
                
                # Extract text
                text = page.extract_text()
                if text:
                    print(f"Text preview: {text[:200]}...")
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    print(f"Found {len(tables)} table(s) on page {page_num}")
                    for table_num, table in enumerate(tables, 1):
                        if table:
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            dataframes.append({
                                'page': page_num,
                                'table_num': table_num,
                                'dataframe': df
                            })
                            print(f"  Table {table_num} shape: {df.shape}")
                            print(f"  Columns: {list(df.columns)}")
                else:
                    print(f"No tables found on page {page_num}")
    
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None
    
    return dataframes

def save_to_csv(dataframes, output_dir="data"):
    """
    Save extracted dataframes to CSV files
    
    Args:
        dataframes: List of dataframe dictionaries
        output_dir: Directory to save CSV files
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for item in dataframes:
        page = item['page']
        table_num = item['table_num']
        df = item['dataframe']
        
        # Generate filename
        filename = f"{output_dir}/page{page}_table{table_num}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved: {filename}")
        saved_files.append(filename)
    
    return saved_files

if __name__ == "__main__":
    # Path to the uploaded PDF
    pdf_path = r"C:\Users\Admin\Downloads\data.pdf"
    
    # Extract data
    dataframes = extract_pdf_data(pdf_path)
    
    if dataframes:
        print(f"\n=== Extraction Summary ===")
        print(f"Total tables extracted: {len(dataframes)}")
        
        # Display first dataframe preview
        if len(dataframes) > 0:
            print("\n=== First Table Preview ===")
            print(dataframes[0]['dataframe'].head())
            print(f"\nShape: {dataframes[0]['dataframe'].shape}")
            print(f"Columns: {list(dataframes[0]['dataframe'].columns)}")
            
        # Save to CSV
        print("\n=== Saving to CSV ===")
        saved_files = save_to_csv(dataframes)
        print(f"\nExtracted {len(saved_files)} CSV file(s)")
    else:
        print("No data extracted from PDF")

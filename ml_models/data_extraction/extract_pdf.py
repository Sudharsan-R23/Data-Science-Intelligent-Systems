"""
PDF Data Extraction Module
Extracts tables from PDF files and converts them to CSV format.
"""

import pandas as pd
import pdfplumber
import camelot
import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract tables from PDF files and convert to CSV."""
    
    def __init__(self, pdf_path, output_dir="data/processed"):
        """
        Initialize PDF Extractor.
        
        Args:
            pdf_path (str): Path to PDF file
            output_dir (str): Output directory for CSV files
        """
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_with_pdfplumber(self):
        """Extract tables using pdfplumber library."""
        tables = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_num, table in enumerate(page_tables):
                            if table:
                                df = pd.DataFrame(table[1:], columns=table[0])
                                tables.append({
                                    'page': page_num + 1,
                                    'table': table_num + 1,
                                    'dataframe': df
                                })
                                logger.info(f"Extracted table {table_num + 1} from page {page_num + 1}")
        except Exception as e:
            logger.error(f"Error extracting with pdfplumber: {str(e)}")
        return tables
    
    def extract_with_camelot(self, flavor='lattice'):
        """
        Extract tables using camelot library.
        
        Args:
            flavor (str): 'lattice' for tables with lines, 'stream' for tables without lines
        """
        tables = []
        try:
            camelot_tables = camelot.read_pdf(self.pdf_path, flavor=flavor, pages='all')
            for idx, table in enumerate(camelot_tables):
                df = table.df
                tables.append({
                    'page': table.page,
                    'table': idx + 1,
                    'dataframe': df
                })
                logger.info(f"Extracted table {idx + 1} from page {table.page}")
        except Exception as e:
            logger.error(f"Error extracting with camelot: {str(e)}")
        return tables
    
    def extract_all_tables(self, method='pdfplumber'):
        """
        Extract all tables from PDF.
        
        Args:
            method (str): 'pdfplumber' or 'camelot'
        
        Returns:
            list: List of extracted tables as DataFrames
        """
        if method == 'pdfplumber':
            tables = self.extract_with_pdfplumber()
        elif method == 'camelot':
            tables = self.extract_with_camelot()
        else:
            raise ValueError("Method must be 'pdfplumber' or 'camelot'")
        
        return tables
    
    def save_to_csv(self, tables, base_filename=None):
        """
        Save extracted tables to CSV files.
        
        Args:
            tables (list): List of table dictionaries
            base_filename (str): Base name for output files
        
        Returns:
            list: List of saved file paths
        """
        if base_filename is None:
            base_filename = Path(self.pdf_path).stem
        
        saved_files = []
        for table_info in tables:
            df = table_info['dataframe']
            page = table_info['page']
            table_num = table_info['table']
            
            filename = f"{base_filename}_page{page}_table{table_num}.csv"
            filepath = self.output_dir / filename
            
            df.to_csv(filepath, index=False)
            saved_files.append(str(filepath))
            logger.info(f"Saved table to {filepath}")
        
        return saved_files
    
    def extract_and_save(self, method='pdfplumber', base_filename=None):
        """
        Extract tables and save to CSV in one step.
        
        Args:
            method (str): Extraction method
            base_filename (str): Base name for output files
        
        Returns:
            list: List of saved file paths
        """
        tables = self.extract_all_tables(method=method)
        if tables:
            return self.save_to_csv(tables, base_filename)
        else:
            logger.warning("No tables found in PDF")
            return []


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_path> [output_dir] [method]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/processed"
    method = sys.argv[3] if len(sys.argv) > 3 else "pdfplumber"
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    extractor = PDFExtractor(pdf_path, output_dir)
    saved_files = extractor.extract_and_save(method=method)
    
    if saved_files:
        print(f"\nSuccessfully extracted {len(saved_files)} tables:")
        for filepath in saved_files:
            print(f"  - {filepath}")
    else:
        print("\nNo tables extracted. Please check the PDF format.")


if __name__ == "__main__":
    main()

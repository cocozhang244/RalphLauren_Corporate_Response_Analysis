"""
Ralph Lauren ESG Analysis - PDF Text Extraction Script
Purpose: Extract text from all PDF documents with precise page number tracking
Output: Individual text files for each document with page markers
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    import fitz  # pymupdf
except ImportError:
    print("PyMuPDF not installed. Installing...")
    os.system("pip install pymupdf")
    import fitz


class PDFTextExtractor:
    """Extract text from PDFs with page-level tracking"""

    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extraction_log = []

    def extract_with_pymupdf(self, pdf_path):
        """Primary extraction method using PyMuPDF"""
        text_by_page = []

        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            for page_num in range(total_pages):
                page = doc[page_num]
                text = page.get_text()

                # Add page marker
                page_marker = f"\n{'='*80}\n[PAGE {page_num + 1} OF {total_pages}]\n{'='*80}\n"
                text_by_page.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'marker': page_marker
                })

            doc.close()
            return text_by_page, "pymupdf", True

        except Exception as e:
            print(f"PyMuPDF extraction failed for {pdf_path.name}: {str(e)}")
            return None, "pymupdf", False

    def extract_text_from_pdf(self, pdf_path):
        """Extract text using PyMuPDF"""
        print(f"\nProcessing: {pdf_path.name}")

        # Extract with PyMuPDF
        text_by_page, method, success = self.extract_with_pymupdf(pdf_path)

        if success and text_by_page:
            print(f"  ✓ Extracted {len(text_by_page)} pages using {method}")
            return text_by_page, method
        else:
            print(f"  ✗ Extraction failed for {pdf_path.name}")
            return None, None

    def save_extracted_text(self, text_by_page, pdf_path, year, doc_type):
        """Save extracted text to file with metadata"""

        # Create safe filename
        safe_name = pdf_path.stem.replace(' ', '_').replace('&', 'and')
        output_file = self.output_dir / f"{year}_{safe_name}_extracted.txt"

        # Create metadata
        metadata = {
            'original_file': pdf_path.name,
            'year': year,
            'document_type': doc_type,
            'total_pages': len(text_by_page),
            'extraction_date': datetime.now().isoformat(),
            'output_file': str(output_file)
        }

        # Write text file with page markers
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"{'#'*80}\n")
            f.write(f"RALPH LAUREN ESG ANALYSIS - EXTRACTED TEXT\n")
            f.write(f"{'#'*80}\n")
            f.write(f"Source File: {pdf_path.name}\n")
            f.write(f"Year: {year}\n")
            f.write(f"Document Type: {doc_type}\n")
            f.write(f"Total Pages: {len(text_by_page)}\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'#'*80}\n\n")

            # Content with page markers
            for page_data in text_by_page:
                f.write(page_data['marker'])
                f.write(page_data['text'])
                f.write("\n")

        # Save metadata JSON
        metadata_file = self.output_dir / f"{year}_{safe_name}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        print(f"  → Saved to: {output_file.name}")

        return metadata

    def categorize_document(self, filename):
        """Determine document type from filename"""
        filename_lower = filename.lower()

        if 'citizenship' in filename_lower or 'gcs' in filename_lower or 'sustainability' in filename_lower:
            return 'Global Citizenship & Sustainability Report'
        elif '10k' in filename_lower or '10-k' in filename_lower:
            return '10-K Annual Report'
        elif 'cdp' in filename_lower and 'climate' in filename_lower:
            return 'CDP Climate Change Disclosure'
        elif 'cdp' in filename_lower and 'water' in filename_lower:
            return 'CDP Water Security Disclosure'
        elif 'cdp' in filename_lower and 'forest' in filename_lower:
            return 'CDP Forest Disclosure'
        elif 'carbon footprint' in filename_lower or 'verification' in filename_lower or 'assurance' in filename_lower:
            return 'Carbon Footprint Verification/Assurance'
        else:
            return 'Other Report'

    def extract_year_from_path(self, pdf_path):
        """Extract year from file path or filename"""
        path_str = str(pdf_path)

        # Check directory name first
        if '2020' in path_str:
            return 2020
        elif '2021' in path_str:
            return 2021
        elif '2022' in path_str:
            return 2022
        elif '2023' in path_str:
            return 2023
        elif '2024' in path_str:
            return 2024
        elif '2025' in path_str:
            return 2025

        # Fallback to filename
        filename = pdf_path.name
        for year in [2020, 2021, 2022, 2023, 2024, 2025]:
            if str(year) in filename:
                return year

        return 'Unknown'

    def process_all_pdfs(self):
        """Process all PDFs in the input directory"""
        print(f"\n{'='*80}")
        print("RALPH LAUREN ESG ANALYSIS - PDF TEXT EXTRACTION")
        print(f"{'='*80}\n")
        print(f"Input Directory: {self.input_dir}")
        print(f"Output Directory: {self.output_dir}\n")

        # Find all PDFs
        pdf_files = list(self.input_dir.rglob('*.pdf'))
        print(f"Found {len(pdf_files)} PDF files to process\n")

        if not pdf_files:
            print("No PDF files found. Please check the input directory.")
            return

        # Process each PDF
        for pdf_path in sorted(pdf_files):
            year = self.extract_year_from_path(pdf_path)
            doc_type = self.categorize_document(pdf_path.name)

            text_by_page, method = self.extract_text_from_pdf(pdf_path)

            if text_by_page:
                metadata = self.save_extracted_text(text_by_page, pdf_path, year, doc_type)
                metadata['extraction_method'] = method
                self.extraction_log.append(metadata)

        # Save extraction log
        self.save_extraction_log()

        print(f"\n{'='*80}")
        print(f"EXTRACTION COMPLETE")
        print(f"{'='*80}")
        print(f"Total files processed: {len(self.extraction_log)}")
        print(f"Output directory: {self.output_dir}")
        print(f"Extraction log: {self.output_dir / 'extraction_log.json'}\n")

    def save_extraction_log(self):
        """Save comprehensive extraction log"""
        log_file = self.output_dir / 'extraction_log.json'

        log_data = {
            'extraction_date': datetime.now().isoformat(),
            'total_files_processed': len(self.extraction_log),
            'files': self.extraction_log
        }

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

        # Also create a human-readable summary
        summary_file = self.output_dir / 'extraction_summary.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("RALPH LAUREN ESG ANALYSIS - EXTRACTION SUMMARY\n")
            f.write("="*80 + "\n\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Files Processed: {len(self.extraction_log)}\n\n")

            # Group by year
            by_year = {}
            for item in self.extraction_log:
                year = item['year']
                if year not in by_year:
                    by_year[year] = []
                by_year[year].append(item)

            for year in sorted(by_year.keys()):
                f.write(f"\n{year}:\n")
                f.write("-" * 40 + "\n")
                for item in by_year[year]:
                    f.write(f"  • {item['document_type']}\n")
                    f.write(f"    File: {item['original_file']}\n")
                    f.write(f"    Pages: {item['total_pages']}\n")
                    f.write(f"    Output: {Path(item['output_file']).name}\n\n")


def main():
    """Main execution function"""
    # Define directories
    input_dir = Path(__file__).parent / 'extracted_reports'
    output_dir = Path(__file__).parent / 'text_extraction_output'

    # Check if input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        print("Please ensure the 'extracted_reports' directory exists with PDF files.")
        return

    # Create extractor and process
    extractor = PDFTextExtractor(input_dir, output_dir)
    extractor.process_all_pdfs()


if __name__ == "__main__":
    main()

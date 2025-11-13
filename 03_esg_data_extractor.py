"""
Ralph Lauren ESG Analysis - Data Extraction Script
Purpose: Extract structured ESG data from extracted text files
Focus: Targets, goals, language patterns, initiatives, commitments
Output: Structured CSV datasets with page references
"""

import os
import re
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import pandas as pd
except ImportError:
    print("pandas not installed. Installing...")
    os.system("pip install pandas")
    import pandas as pd


class ESGDataExtractor:
    """Extract structured ESG data from text files"""

    def __init__(self, text_dir, output_dir):
        self.text_dir = Path(text_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize data containers
        self.targets_data = []
        self.language_data = []
        self.initiatives_data = []
        self.commitments_data = []
        self.impact_areas_data = []

        # Define keywords and patterns
        self.define_patterns()

    def define_patterns(self):
        """Define regex patterns and keywords for extraction"""

        # Target-related keywords
        self.target_keywords = [
            r'target',
            r'goal',
            r'objective',
            r'aim to',
            r'reduce.*by \d+%',
            r'achieve.*by \d{4}',
            r'reach.*by \d{4}',
            r'\d+% reduction',
            r'net zero',
            r'carbon neutral',
            r'science-based target'
        ]

        # Commitment strength indicators
        self.commitment_strong = [
            'committed to', 'will achieve', 'will reduce', 'will reach',
            'pledge to', 'determined to', 'dedicated to', 'have committed'
        ]

        self.commitment_moderate = [
            'plan to', 'intend to', 'aim to', 'working to', 'seeking to',
            'strive to', 'expect to', 'focused on'
        ]

        self.commitment_weak = [
            'aspire to', 'hope to', 'may', 'could', 'exploring',
            'considering', 'evaluating', 'subject to', 'dependent on'
        ]

        # Initiative keywords
        self.initiative_keywords = [
            r'program', r'initiative', r'partnership', r'collaboration',
            r'launched', r'announced', r'introduced', r'implemented',
            r'invested \$[\d,]+', r'investment of', r'million', r'billion'
        ]

        # Impact area keywords
        self.impact_keywords = {
            'Climate/Carbon': ['emission', 'carbon', 'greenhouse gas', 'GHG', 'CO2', 'climate',
                               'scope 1', 'scope 2', 'scope 3', 'carbon footprint'],
            'Water': ['water', 'H2O', 'water use', 'water consumption', 'water stewardship',
                      'water stress', 'water efficiency'],
            'Waste/Circular Economy': ['waste', 'recycl', 'circular', 'zero waste', 'landfill',
                                        'reuse', 'repurpose', 'end-of-life'],
            'Energy': ['energy', 'renewable energy', 'solar', 'wind', 'renewable',
                       'energy efficiency', 'electricity'],
            'Materials': ['sustainable material', 'organic cotton', 'recycled polyester',
                          'preferred fiber', 'sustainable sourcing', 'material innovation'],
            'Supply Chain': ['supplier', 'supply chain', 'factory', 'manufacturing',
                            'vendor', 'sourcing'],
            'Human Rights/Labor': ['human rights', 'labor', 'worker', 'fair wage',
                                   'working conditions', 'child labor', 'forced labor'],
            'Diversity/Equity': ['diversity', 'equity', 'inclusion', 'DEI', 'gender',
                                'racial', 'equal opportunity', 'representation'],
            'Biodiversity': ['biodiversity', 'ecosystem', 'nature', 'forest', 'deforestation',
                            'land use', 'habitat'],
            'Governance': ['governance', 'board', 'oversight', 'policy', 'compliance',
                          'ethics', 'transparency', 'disclosure']
        }

        # Numeric patterns
        self.numeric_patterns = {
            'percentage': r'(\d+(?:\.\d+)?)\s*%',
            'year': r'\b(20\d{2})\b',
            'currency': r'\$\s*([\d,]+(?:\.\d+)?)\s*(million|billion|M|B)?',
            'metric_ton': r'([\d,]+(?:\.\d+)?)\s*(?:metric\s*)?(?:ton|tonne)s?',
            'reduction': r'(\d+(?:\.\d+)?)\s*%\s*reduction'
        }

    def parse_text_file(self, file_path):
        """Parse extracted text file and return structured content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from header
        metadata = self.extract_metadata_from_header(content)

        # Split by page markers
        page_pattern = r'={80}\n\[PAGE (\d+) OF (\d+)\]\n={80}'
        pages = re.split(page_pattern, content)

        # Structure: [header, page1_num, total_pages, page1_text, page2_num, total_pages, page2_text, ...]
        structured_pages = []
        for i in range(1, len(pages), 3):
            if i + 2 <= len(pages):
                page_data = {
                    'page_number': int(pages[i]),
                    'total_pages': int(pages[i + 1]),
                    'text': pages[i + 2]
                }
                structured_pages.append(page_data)

        return metadata, structured_pages

    def extract_metadata_from_header(self, content):
        """Extract metadata from file header"""
        metadata = {}

        # Extract from header section
        header_match = re.search(r'Source File: (.+?)\n', content)
        if header_match:
            metadata['source_file'] = header_match.group(1).strip()

        year_match = re.search(r'Year: (.+?)\n', content)
        if year_match:
            metadata['year'] = year_match.group(1).strip()

        doc_type_match = re.search(r'Document Type: (.+?)\n', content)
        if doc_type_match:
            metadata['document_type'] = doc_type_match.group(1).strip()

        return metadata

    def extract_targets_and_goals(self, pages, metadata):
        """Extract specific targets and goals with page references"""
        for page in pages:
            page_num = page['page_number']
            text = page['text']

            # Search for target-related text
            for pattern in self.target_keywords:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Get context (surrounding text)
                    start = max(0, match.start() - 200)
                    end = min(len(text), match.end() + 200)
                    context = text[start:end].strip()

                    # Clean up context
                    context = ' '.join(context.split())

                    # Extract numeric values if present
                    percentages = re.findall(self.numeric_patterns['percentage'], context)
                    years = re.findall(self.numeric_patterns['year'], context)

                    target_entry = {
                        'year': metadata.get('year', 'Unknown'),
                        'document': metadata.get('document_type', 'Unknown'),
                        'source_file': metadata.get('source_file', 'Unknown'),
                        'page_number': page_num,
                        'target_text': context[:300],  # Limit context length
                        'percentages': ', '.join(percentages) if percentages else '',
                        'target_years': ', '.join(years) if years else '',
                        'keyword_matched': match.group()
                    }

                    self.targets_data.append(target_entry)

    def extract_language_patterns(self, pages, metadata):
        """Analyze commitment language strength"""
        for page in pages:
            page_num = page['page_number']
            text = page['text']

            # Check for strong commitments
            for phrase in self.commitment_strong:
                if phrase in text.lower():
                    matches = re.finditer(re.escape(phrase), text, re.IGNORECASE)
                    for match in matches:
                        start = max(0, match.start() - 150)
                        end = min(len(text), match.end() + 150)
                        context = ' '.join(text[start:end].split())

                        self.language_data.append({
                            'year': metadata.get('year', 'Unknown'),
                            'document': metadata.get('document_type', 'Unknown'),
                            'page_number': page_num,
                            'commitment_strength': 'Strong',
                            'phrase': match.group(),
                            'context': context[:250]
                        })

            # Check for moderate commitments
            for phrase in self.commitment_moderate:
                if phrase in text.lower():
                    matches = re.finditer(re.escape(phrase), text, re.IGNORECASE)
                    for match in matches:
                        start = max(0, match.start() - 150)
                        end = min(len(text), match.end() + 150)
                        context = ' '.join(text[start:end].split())

                        self.language_data.append({
                            'year': metadata.get('year', 'Unknown'),
                            'document': metadata.get('document_type', 'Unknown'),
                            'page_number': page_num,
                            'commitment_strength': 'Moderate',
                            'phrase': match.group(),
                            'context': context[:250]
                        })

            # Check for weak/hedging language
            for phrase in self.commitment_weak:
                if phrase in text.lower():
                    matches = re.finditer(re.escape(phrase), text, re.IGNORECASE)
                    for match in matches:
                        start = max(0, match.start() - 150)
                        end = min(len(text), match.end() + 150)
                        context = ' '.join(text[start:end].split())

                        self.language_data.append({
                            'year': metadata.get('year', 'Unknown'),
                            'document': metadata.get('document_type', 'Unknown'),
                            'page_number': page_num,
                            'commitment_strength': 'Weak/Hedging',
                            'phrase': match.group(),
                            'context': context[:250]
                        })

    def extract_initiatives(self, pages, metadata):
        """Extract announced initiatives and programs"""
        for page in pages:
            page_num = page['page_number']
            text = page['text']

            for pattern in self.initiative_keywords:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 200)
                    end = min(len(text), match.end() + 200)
                    context = ' '.join(text[start:end].split())

                    # Extract financial information if present
                    currency_match = re.search(self.numeric_patterns['currency'], context)
                    investment_amount = ''
                    if currency_match:
                        investment_amount = currency_match.group()

                    self.initiatives_data.append({
                        'year': metadata.get('year', 'Unknown'),
                        'document': metadata.get('document_type', 'Unknown'),
                        'page_number': page_num,
                        'initiative_text': context[:300],
                        'keyword_matched': match.group(),
                        'investment_amount': investment_amount
                    })

    def extract_impact_areas(self, pages, metadata):
        """Extract mentions of different ESG impact areas"""
        for page in pages:
            page_num = page['page_number']
            text = page['text'].lower()

            for impact_area, keywords in self.impact_keywords.items():
                for keyword in keywords:
                    pattern = re.escape(keyword.lower())
                    matches = list(re.finditer(pattern, text))

                    if matches:
                        # Count occurrences
                        count = len(matches)

                        # Get one example context
                        match = matches[0]
                        start = max(0, match.start() - 100)
                        end = min(len(text), match.end() + 100)
                        context = ' '.join(text[start:end].split())

                        self.impact_areas_data.append({
                            'year': metadata.get('year', 'Unknown'),
                            'document': metadata.get('document_type', 'Unknown'),
                            'page_number': page_num,
                            'impact_area': impact_area,
                            'keyword': keyword,
                            'occurrence_count': count,
                            'example_context': context[:200]
                        })

    def process_all_text_files(self):
        """Process all extracted text files"""
        print(f"\n{'='*80}")
        print("RALPH LAUREN ESG ANALYSIS - DATA EXTRACTION")
        print(f"{'='*80}\n")

        text_files = list(self.text_dir.glob('*_extracted.txt'))
        print(f"Found {len(text_files)} text files to process\n")

        if not text_files:
            print("No extracted text files found.")
            print(f"Please run 02_pdf_text_extractor.py first.")
            return

        for file_path in sorted(text_files):
            print(f"Processing: {file_path.name}")

            try:
                metadata, pages = self.parse_text_file(file_path)

                # Extract different data types
                self.extract_targets_and_goals(pages, metadata)
                self.extract_language_patterns(pages, metadata)
                self.extract_initiatives(pages, metadata)
                self.extract_impact_areas(pages, metadata)

                print(f"  ✓ Extracted data from {len(pages)} pages")

            except Exception as e:
                print(f"  ✗ Error processing {file_path.name}: {str(e)}")

        # Save all extracted data
        self.save_all_data()

    def save_all_data(self):
        """Save all extracted data to CSV files"""
        print(f"\n{'='*80}")
        print("SAVING EXTRACTED DATA")
        print(f"{'='*80}\n")

        # Save targets data
        if self.targets_data:
            targets_df = pd.DataFrame(self.targets_data)
            targets_file = self.output_dir / 'extracted_targets_goals.csv'
            targets_df.to_csv(targets_file, index=False)
            print(f"✓ Saved {len(self.targets_data)} target entries to: {targets_file.name}")

        # Save language data
        if self.language_data:
            language_df = pd.DataFrame(self.language_data)
            language_file = self.output_dir / 'extracted_language_patterns.csv'
            language_df.to_csv(language_file, index=False)
            print(f"✓ Saved {len(self.language_data)} language entries to: {language_file.name}")

        # Save initiatives data
        if self.initiatives_data:
            initiatives_df = pd.DataFrame(self.initiatives_data)
            initiatives_file = self.output_dir / 'extracted_initiatives.csv'
            initiatives_df.to_csv(initiatives_file, index=False)
            print(f"✓ Saved {len(self.initiatives_data)} initiative entries to: {initiatives_file.name}")

        # Save impact areas data
        if self.impact_areas_data:
            impact_df = pd.DataFrame(self.impact_areas_data)
            impact_file = self.output_dir / 'extracted_impact_areas.csv'
            impact_df.to_csv(impact_file, index=False)
            print(f"✓ Saved {len(self.impact_areas_data)} impact area entries to: {impact_file.name}")

        # Create summary statistics
        self.create_summary_statistics()

    def create_summary_statistics(self):
        """Create summary statistics report"""
        summary_file = self.output_dir / 'extraction_statistics.txt'

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("RALPH LAUREN ESG ANALYSIS - EXTRACTION STATISTICS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"Total Targets/Goals Extracted: {len(self.targets_data)}\n")
            f.write(f"Total Language Patterns Identified: {len(self.language_data)}\n")
            f.write(f"Total Initiatives Cataloged: {len(self.initiatives_data)}\n")
            f.write(f"Total Impact Area Mentions: {len(self.impact_areas_data)}\n\n")

            # Breakdown by year
            if self.targets_data:
                targets_df = pd.DataFrame(self.targets_data)
                f.write("\nTargets by Year:\n")
                f.write("-"*40 + "\n")
                year_counts = targets_df['year'].value_counts().sort_index()
                for year, count in year_counts.items():
                    f.write(f"  {year}: {count}\n")

            if self.language_data:
                language_df = pd.DataFrame(self.language_data)
                f.write("\nLanguage Patterns by Strength:\n")
                f.write("-"*40 + "\n")
                strength_counts = language_df['commitment_strength'].value_counts()
                for strength, count in strength_counts.items():
                    f.write(f"  {strength}: {count}\n")

            if self.impact_areas_data:
                impact_df = pd.DataFrame(self.impact_areas_data)
                f.write("\nTop Impact Areas Mentioned:\n")
                f.write("-"*40 + "\n")
                area_counts = impact_df.groupby('impact_area')['occurrence_count'].sum().sort_values(ascending=False)
                for area, count in area_counts.head(10).items():
                    f.write(f"  {area}: {count} mentions\n")

        print(f"✓ Saved summary statistics to: {summary_file.name}")
        print(f"\nAll data saved to: {self.output_dir}\n")


def main():
    """Main execution function"""
    text_dir = Path(__file__).parent / 'text_extraction_output'
    output_dir = Path(__file__).parent / 'structured_data_output'

    if not text_dir.exists():
        print(f"Error: Text extraction directory not found: {text_dir}")
        print("Please run 02_pdf_text_extractor.py first.")
        return

    extractor = ESGDataExtractor(text_dir, output_dir)
    extractor.process_all_text_files()


if __name__ == "__main__":
    main()

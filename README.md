# Ralph Lauren ESG Corporate Response Analysis

## Project Overview

This project analyzes Ralph Lauren's corporate response to regulatory and policy shifts in ESG (Environmental, Social, Governance) from 2020-2025, with particular focus on changes in the U.S. (red vs. blue states) and EU policy landscapes.

**Client Objective**: Identify visible corporate responses to regulatory/policy shifts through analysis of:
- Target setting and goal changes
- Language usage and intended tone
- Announced initiatives
- Commitment retreats or modifications
- Impact area focus shifts

## Data Sources

### Documents Analyzed (2020-2025):
- **Global Citizenship & Sustainability Reports** (Annual)
- **10-K Annual Reports** (SEC Filings)
- **CDP Disclosures** (Climate Change, Water Security, Forests)
- **Carbon Footprint Verification Statements**

**Total Documents**: 20+ comprehensive reports spanning 6 years

## Project Structure

```
RalphLauren_Corporate_Response_Analysis/
│
├── 00_RUN_ALL_ANALYSIS.py              # Master script - runs entire pipeline
├── 01_ANALYTICAL_FRAMEWORK.md          # Detailed methodology documentation
├── 02_pdf_text_extractor.py            # PDF text extraction with page tracking
├── 03_esg_data_extractor.py            # Structured data extraction
├── 04_quantitative_analysis_visualization.py  # Analysis & charts
│
├── extracted_reports/                   # Original PDF files (organized by year)
│   ├── Ralph Lauren 2020 Disclosures/
│   ├── Ralph Lauren 2021 Disclousures/
│   ├── Ralph Lauren 2022 Disclousures/
│   ├── Ralph Lauren 2023 Disclousures/
│   ├── Ralph_Lauren_2024/
│   └── Ralph Lauren 2025 Disclousures/
│
├── text_extraction_output/             # Extracted text with page markers
│   ├── *_extracted.txt                 # Full text files with page numbers
│   ├── *_metadata.json                 # Extraction metadata
│   └── extraction_log.json             # Complete extraction log
│
├── structured_data_output/             # Structured datasets (CSV format)
│   ├── extracted_targets_goals.csv     # All targets with page references
│   ├── extracted_language_patterns.csv # Language analysis with context
│   ├── extracted_initiatives.csv       # Initiative catalog
│   ├── extracted_impact_areas.csv      # Impact area mentions
│   └── extraction_statistics.txt       # Summary statistics
│
└── analysis_output/                    # Final analysis deliverables
    ├── charts/                         # Visualizations (PNG format)
    │   ├── targets_by_year.png
    │   ├── commitment_language_over_time.png
    │   ├── initiatives_over_time.png
    │   ├── impact_areas_heatmap.png
    │   ├── top_impact_areas_trends.png
    │   └── comprehensive_dashboard.png
    │
    ├── tables/                         # Data tables (CSV format)
    │   ├── targets_by_year_summary.csv
    │   ├── commitment_language_counts.csv
    │   └── impact_areas_by_year.csv
    │
    └── analysis_summary_report.txt     # Executive summary
```

## Quick Start Guide

### Prerequisites

```bash
# Required Python packages (automatically installed by scripts):
- PyMuPDF (fitz)
- pdfplumber
- pandas
- numpy
- matplotlib
- seaborn
```

### Running the Complete Analysis

**Option 1: Run Everything at Once**
```bash
python 00_RUN_ALL_ANALYSIS.py
```

**Option 2: Run Scripts Individually**
```bash
# Step 1: Extract text from PDFs
python 02_pdf_text_extractor.py

# Step 2: Extract structured ESG data
python 03_esg_data_extractor.py

# Step 3: Perform quantitative analysis and create visualizations
python 04_quantitative_analysis_visualization.py
```

## Methodology

### Phase 1: Text Extraction (Script 02)
- Extracts all text from PDF documents
- Maintains precise page number tracking
- Creates searchable text corpus with metadata
- Generates extraction logs for quality assurance

**Output**: `text_extraction_output/` directory with text files and metadata

### Phase 2: Structured Data Extraction (Script 03)
Extracts five key data categories:

1. **Targets & Goals**: Numeric targets, timelines, baseline years, progress metrics
2. **Language Patterns**: Commitment strength (strong/moderate/weak), hedging language
3. **Initiatives**: New programs, partnerships, investments, implementation plans
4. **Commitments**: Modifications, retreats, delayed timelines, scope changes
5. **Impact Areas**: 10 ESG categories with mention frequency tracking

**Output**: `structured_data_output/` with CSV files containing page-referenced data

### Phase 3: Quantitative Analysis (Script 04)
- Year-over-year trend analysis
- Commitment language strength evolution
- Initiative announcement patterns
- Impact area focus shifts
- Comprehensive visualizations

**Output**: `analysis_output/` with charts, tables, and summary report

## Key Features

### Page-Level Tracking
Every extracted data point includes exact page references in format:
- `[Document_Year]:[Page Number]`
- Example: "GCS_2022:45" or "10K_2023:78"

This enables:
- Cross-referencing and quality checks
- Source verification
- Audit trail for all findings

### Dual Extraction Methods
- **Primary**: PyMuPDF (fast, accurate)
- **Backup**: pdfplumber (handles complex layouts)
- Automatic fallback ensures robust extraction

### Comprehensive Pattern Matching
Uses regex patterns and keyword dictionaries to identify:
- Target keywords (34+ patterns)
- Commitment language (3 strength levels)
- Initiative indicators
- ESG impact areas (10 categories, 90+ keywords)

### Professional Visualizations
- High-resolution charts (300 DPI)
- Publication-ready formatting
- Multiple chart types (bar, line, heatmap, pie, dashboard)
- Color-coded for clarity

## Deliverables

### 1. Extracted Text Files
- Full document text with page markers
- Metadata JSON for each document
- Extraction log with statistics

### 2. Structured Datasets (CSV)
All datasets include:
- Year
- Document type
- Page number(s)
- Specific finding
- Context quote
- Quantitative values (where applicable)

**Files**:
- `extracted_targets_goals.csv`
- `extracted_language_patterns.csv`
- `extracted_initiatives.csv`
- `extracted_impact_areas.csv`

### 3. Analysis Visualizations (PNG)
- Targets by year (bar chart)
- Commitment language evolution (stacked bar)
- Initiative trends (line chart)
- Impact areas heatmap
- Top impact areas trends
- Comprehensive dashboard (6-panel)

### 4. Summary Tables (CSV)
- Year-over-year changes
- Percentage distributions
- Statistical summaries

### 5. Analytical Reports (TXT)
- Executive summary
- Key metrics
- Trend analysis
- Document type breakdown

## Analysis Principles

### Objectivity
- Evidence-based findings
- Counterevidence included
- Clear distinction between observation and interpretation
- Documented limitations

### Precision
- Exact page citations
- Direct quotes for language analysis
- Specific numeric values with units
- Clear date and version tracking

### Comprehensiveness
- Systematic coverage of all documents
- No cherry-picking
- Positive and negative findings included
- Gaps documented

### Transparency
- Fully documented methodology
- All sources cited
- Assumptions explicit
- Limitations acknowledged

## Data Quality Assurance

### Automated Checks
- Extraction validation logs
- Duplicate detection
- Missing data identification
- Statistical outlier flagging

### Manual Verification Points
1. Spot-check extracted text against original PDFs
2. Validate high-impact findings
3. Cross-reference year-over-year claims
4. Verify quantitative metrics

### Audit Trail
Every finding traceable to:
- Specific document
- Exact page number
- Original context
- Extraction timestamp

## Policy Context Timeline

### U.S. Policy Landscape
- **2020-2021**: Trump to Biden administration transition
- **2021**: Rejoining Paris Agreement, Infrastructure Bill
- **2022**: Inflation Reduction Act, SEC climate disclosure proposals
- **2023**: State-level policy divergence (red vs. blue)
- **2024-2025**: Potential regulatory shifts

### EU Policy Landscape
- **2020**: EU Green Deal launch
- **2021**: EU Taxonomy Regulation
- **2022**: CSRD (Corporate Sustainability Reporting Directive)
- **2023**: SFDR implementation, supply chain due diligence
- **2024-2025**: ESRS standards, deforestation regulation

## Customization Options

### Adjust Keyword Patterns
Edit `03_esg_data_extractor.py`, method `define_patterns()` to:
- Add new keywords
- Modify regex patterns
- Adjust impact area categories

### Modify Visualizations
Edit `04_quantitative_analysis_visualization.py` to:
- Change color schemes
- Adjust chart types
- Add new analysis dimensions

### Extend Analysis
Additional scripts can be created for:
- Geographic-specific analysis (U.S. vs EU)
- Sentiment analysis
- Network analysis of initiatives
- Predictive modeling

## Troubleshooting

### Issue: "No PDF files found"
**Solution**: Ensure `extracted_reports/` directory contains PDF files

### Issue: "PyMuPDF installation failed"
**Solution**: Install manually: `pip install PyMuPDF`

### Issue: "Charts not generating"
**Solution**: Install matplotlib: `pip install matplotlib seaborn`

### Issue: "Extraction quality issues"
**Solution**: Check PDF quality; use manual verification for critical sections

## Next Steps for Deep Analysis

1. **Geographic Divergence Analysis**: Compare U.S. vs. EU language
2. **Temporal Correlation**: Map corporate responses to specific policy events
3. **Commitment Tracking**: Track specific targets across all years
4. **Risk Disclosure Analysis**: Analyze climate risk language in 10-Ks
5. **Materiality Assessment**: Identify which impact areas receive most focus

## Contact & Support

For questions or issues:
1. Review `01_ANALYTICAL_FRAMEWORK.md` for detailed methodology
2. Check extraction logs in output directories
3. Verify all prerequisites are installed
4. Consult script comments for technical details

## Version History

- **Version 1.0** (November 2025): Initial release
  - Complete extraction pipeline
  - Structured data outputs
  - Quantitative analysis and visualization
  - Comprehensive documentation

## License & Usage

This analysis framework is designed for corporate ESG research and policy analysis. All methodologies are transparent and reproducible for audit purposes.

---

**Generated**: November 2025
**Analysis Period**: 2020-2025
**Company**: Ralph Lauren Corporation
**Focus**: ESG Corporate Response to Policy Shifts

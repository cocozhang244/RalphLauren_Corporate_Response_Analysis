"""
Ralph Lauren ESG Corporate Response Analysis - Master Script
Purpose: Run all analysis steps in sequence
Author: ESG Analysis Team
Date: November 2025
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class MasterAnalysisRunner:
    """Orchestrate the complete analysis pipeline"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.scripts = [
            ('02_pdf_text_extractor.py', 'PDF Text Extraction'),
            ('03_esg_data_extractor.py', 'ESG Data Extraction'),
            ('04_quantitative_analysis_visualization.py', 'Quantitative Analysis & Visualization')
        ]

    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*80}")
        print(text)
        print(f"{'='*80}\n")

    def run_script(self, script_name, description):
        """Run a Python script and handle errors"""
        self.print_header(f"STEP: {description}")
        print(f"Running: {script_name}\n")

        script_path = self.base_dir / script_name

        if not script_path.exists():
            print(f"ERROR: Script not found: {script_name}")
            return False

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )

            # Print output
            if result.stdout:
                print(result.stdout)

            if result.stderr:
                print("STDERR:", result.stderr)

            if result.returncode == 0:
                print(f"\n✓ {description} completed successfully")
                return True
            else:
                print(f"\n✗ {description} failed with return code {result.returncode}")
                return False

        except Exception as e:
            print(f"\n✗ Error running {script_name}: {str(e)}")
            return False

    def check_prerequisites(self):
        """Check if required directories and files exist"""
        self.print_header("CHECKING PREREQUISITES")

        extracted_reports = self.base_dir / 'extracted_reports'

        if not extracted_reports.exists():
            print("✗ ERROR: 'extracted_reports' directory not found")
            print("Please ensure PDF files are extracted first.")
            return False

        pdf_files = list(extracted_reports.rglob('*.pdf'))
        print(f"✓ Found {len(pdf_files)} PDF files in extracted_reports/")

        if len(pdf_files) == 0:
            print("✗ ERROR: No PDF files found to analyze")
            return False

        return True

    def create_analysis_log(self, success_steps, failed_steps):
        """Create analysis execution log"""
        log_file = self.base_dir / 'analysis_execution_log.txt'

        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RALPH LAUREN ESG CORPORATE RESPONSE ANALYSIS\n")
            f.write("MASTER ANALYSIS EXECUTION LOG\n")
            f.write("="*80 + "\n\n")
            f.write(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("COMPLETED STEPS:\n")
            f.write("-"*80 + "\n")
            for step in success_steps:
                f.write(f"  ✓ {step}\n")
            f.write("\n")

            if failed_steps:
                f.write("FAILED STEPS:\n")
                f.write("-"*80 + "\n")
                for step in failed_steps:
                    f.write(f"  ✗ {step}\n")
                f.write("\n")

            # Output directories
            f.write("OUTPUT DIRECTORIES:\n")
            f.write("-"*80 + "\n")
            f.write(f"  Text Extraction: text_extraction_output/\n")
            f.write(f"  Structured Data: structured_data_output/\n")
            f.write(f"  Analysis Results: analysis_output/\n")
            f.write(f"    - Charts: analysis_output/charts/\n")
            f.write(f"    - Tables: analysis_output/tables/\n")

        print(f"\n✓ Analysis log saved to: {log_file.name}")

    def run_complete_analysis(self):
        """Run all analysis steps"""
        self.print_header("RALPH LAUREN ESG CORPORATE RESPONSE ANALYSIS")
        print("Master Analysis Pipeline")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Check prerequisites
        if not self.check_prerequisites():
            print("\nAnalysis cannot proceed. Please fix the issues above.")
            return

        # Run each script
        success_steps = []
        failed_steps = []

        for script_name, description in self.scripts:
            success = self.run_script(script_name, description)

            if success:
                success_steps.append(description)
            else:
                failed_steps.append(description)
                print(f"\nWARNING: {description} failed. Continuing with next step...")

        # Create execution log
        self.create_analysis_log(success_steps, failed_steps)

        # Final summary
        self.print_header("ANALYSIS PIPELINE COMPLETE")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nSuccessful Steps: {len(success_steps)}/{len(self.scripts)}")
        print(f"Failed Steps: {len(failed_steps)}/{len(self.scripts)}\n")

        if failed_steps:
            print("⚠ Some steps failed. Please review the output above.")
        else:
            print("✓ All analysis steps completed successfully!")

        print("\nOutput Locations:")
        print("  • Extracted Text: text_extraction_output/")
        print("  • Structured Data: structured_data_output/")
        print("  • Analysis Results: analysis_output/")
        print("    - Charts: analysis_output/charts/")
        print("    - Tables: analysis_output/tables/")
        print("    - Summary: analysis_output/analysis_summary_report.txt")
        print("\n")


def main():
    """Main execution"""
    runner = MasterAnalysisRunner()
    runner.run_complete_analysis()


if __name__ == "__main__":
    main()

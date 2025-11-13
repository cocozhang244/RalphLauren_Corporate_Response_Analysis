"""
Ralph Lauren ESG Analysis - Quantitative Analysis & Visualization Script
Purpose: Analyze extracted data and create visualizations
Output: Charts, graphs, tables showing trends and patterns
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Installing required packages...")
    os.system("pip install pandas numpy")
    import pandas as pd
    import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
except ImportError:
    print("Installing visualization packages...")
    os.system("pip install matplotlib seaborn")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class ESGAnalyzer:
    """Analyze ESG data and create visualizations"""

    def __init__(self, data_dir, output_dir):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.charts_dir = self.output_dir / 'charts'
        self.tables_dir = self.output_dir / 'tables'
        self.charts_dir.mkdir(exist_ok=True)
        self.tables_dir.mkdir(exist_ok=True)

        # Load data
        self.load_data()

    def load_data(self):
        """Load all extracted data files"""
        print(f"\n{'='*80}")
        print("LOADING EXTRACTED DATA")
        print(f"{'='*80}\n")

        try:
            self.targets_df = pd.read_csv(self.data_dir / 'extracted_targets_goals.csv')
            print(f"✓ Loaded {len(self.targets_df)} target entries")
        except FileNotFoundError:
            print("✗ Targets file not found")
            self.targets_df = pd.DataFrame()

        try:
            self.language_df = pd.read_csv(self.data_dir / 'extracted_language_patterns.csv')
            print(f"✓ Loaded {len(self.language_df)} language entries")
        except FileNotFoundError:
            print("✗ Language file not found")
            self.language_df = pd.DataFrame()

        try:
            self.initiatives_df = pd.read_csv(self.data_dir / 'extracted_initiatives.csv')
            print(f"✓ Loaded {len(self.initiatives_df)} initiative entries")
        except FileNotFoundError:
            print("✗ Initiatives file not found")
            self.initiatives_df = pd.DataFrame()

        try:
            self.impact_df = pd.read_csv(self.data_dir / 'extracted_impact_areas.csv')
            print(f"✓ Loaded {len(self.impact_df)} impact area entries")
        except FileNotFoundError:
            print("✗ Impact areas file not found")
            self.impact_df = pd.DataFrame()

    def analyze_targets_over_time(self):
        """Analyze how targets mentioned change over time"""
        if self.targets_df.empty:
            print("No targets data available")
            return

        print("\n" + "="*80)
        print("ANALYZING TARGETS OVER TIME")
        print("="*80)

        # Convert year to numeric, handling 'Unknown' values
        self.targets_df['year_numeric'] = pd.to_numeric(self.targets_df['year'], errors='coerce')

        # Count targets by year
        targets_by_year = self.targets_df['year_numeric'].value_counts().sort_index()

        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(targets_by_year.index, targets_by_year.values, color='steelblue', alpha=0.8, edgecolor='navy')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')

        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Target/Goal Mentions', fontsize=12, fontweight='bold')
        ax.set_title('Ralph Lauren: ESG Targets and Goals Mentions by Year', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        chart_file = self.charts_dir / 'targets_by_year.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: {chart_file.name}")
        plt.close()

        # Create summary table
        summary_table = pd.DataFrame({
            'Year': targets_by_year.index,
            'Target Mentions': targets_by_year.values
        })

        # Calculate year-over-year change
        summary_table['YoY Change'] = summary_table['Target Mentions'].diff()
        summary_table['YoY % Change'] = summary_table['Target Mentions'].pct_change() * 100

        table_file = self.tables_dir / 'targets_by_year_summary.csv'
        summary_table.to_csv(table_file, index=False)
        print(f"✓ Saved table: {table_file.name}")

    def analyze_commitment_language(self):
        """Analyze commitment language strength over time"""
        if self.language_df.empty:
            print("No language data available")
            return

        print("\n" + "="*80)
        print("ANALYZING COMMITMENT LANGUAGE PATTERNS")
        print("="*80)

        # Convert year to numeric
        self.language_df['year_numeric'] = pd.to_numeric(self.language_df['year'], errors='coerce')

        # Count by strength and year
        language_by_year_strength = self.language_df.groupby(['year_numeric', 'commitment_strength']).size().unstack(fill_value=0)

        # Create stacked bar chart
        fig, ax = plt.subplots(figsize=(12, 6))

        colors = {'Strong': '#2E7D32', 'Moderate': '#FFA726', 'Weak/Hedging': '#D32F2F'}
        language_by_year_strength.plot(kind='bar', stacked=True, ax=ax,
                                       color=[colors.get(col, 'gray') for col in language_by_year_strength.columns])

        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Commitment Phrases', fontsize=12, fontweight='bold')
        ax.set_title('Ralph Lauren: Commitment Language Strength Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.legend(title='Commitment Strength', title_fontsize=11, fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=0)

        plt.tight_layout()
        chart_file = self.charts_dir / 'commitment_language_over_time.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: {chart_file.name}")
        plt.close()

        # Calculate percentages
        language_pct = language_by_year_strength.div(language_by_year_strength.sum(axis=1), axis=0) * 100

        # Save summary tables
        table_file_counts = self.tables_dir / 'commitment_language_counts.csv'
        language_by_year_strength.to_csv(table_file_counts)
        print(f"✓ Saved table: {table_file_counts.name}")

        table_file_pct = self.tables_dir / 'commitment_language_percentages.csv'
        language_pct.to_csv(table_file_pct)
        print(f"✓ Saved table: {table_file_pct.name}")

    def analyze_initiatives(self):
        """Analyze initiatives announced over time"""
        if self.initiatives_df.empty:
            print("No initiatives data available")
            return

        print("\n" + "="*80)
        print("ANALYZING INITIATIVES")
        print("="*80)

        # Convert year to numeric
        self.initiatives_df['year_numeric'] = pd.to_numeric(self.initiatives_df['year'], errors='coerce')

        # Count initiatives by year
        initiatives_by_year = self.initiatives_df['year_numeric'].value_counts().sort_index()

        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(initiatives_by_year.index, initiatives_by_year.values, marker='o', linewidth=2,
               markersize=10, color='#1976D2', markerfacecolor='#BBDEFB', markeredgewidth=2)

        # Add value labels
        for x, y in zip(initiatives_by_year.index, initiatives_by_year.values):
            ax.text(x, y + max(initiatives_by_year.values)*0.03, f'{int(y)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)

        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Initiative Mentions', fontsize=12, fontweight='bold')
        ax.set_title('Ralph Lauren: ESG Initiative Announcements Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.grid(alpha=0.3)

        plt.tight_layout()
        chart_file = self.charts_dir / 'initiatives_over_time.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: {chart_file.name}")
        plt.close()

    def analyze_impact_areas(self):
        """Analyze ESG impact area focus over time"""
        if self.impact_df.empty:
            print("No impact areas data available")
            return

        print("\n" + "="*80)
        print("ANALYZING IMPACT AREAS")
        print("="*80)

        # Convert year to numeric
        self.impact_df['year_numeric'] = pd.to_numeric(self.impact_df['year'], errors='coerce')

        # Aggregate occurrence counts by impact area and year
        impact_by_year = self.impact_df.groupby(['year_numeric', 'impact_area'])['occurrence_count'].sum().unstack(fill_value=0)

        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(impact_by_year.T, annot=True, fmt='g', cmap='YlOrRd', cbar_kws={'label': 'Mention Count'},
                   linewidths=0.5, ax=ax)

        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Impact Area', fontsize=12, fontweight='bold')
        ax.set_title('Ralph Lauren: ESG Impact Area Focus Over Time (Heatmap)', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        chart_file = self.charts_dir / 'impact_areas_heatmap.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: {chart_file.name}")
        plt.close()

        # Create line chart for top impact areas
        top_areas = self.impact_df.groupby('impact_area')['occurrence_count'].sum().nlargest(5).index

        fig, ax = plt.subplots(figsize=(12, 6))
        for area in top_areas:
            area_data = impact_by_year[area]
            ax.plot(area_data.index, area_data.values, marker='o', linewidth=2, label=area, markersize=8)

        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mention Count', fontsize=12, fontweight='bold')
        ax.set_title('Ralph Lauren: Top 5 ESG Impact Areas - Trends Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.legend(title='Impact Area', loc='best', fontsize=10)
        ax.grid(alpha=0.3)

        plt.tight_layout()
        chart_file = self.charts_dir / 'top_impact_areas_trends.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved chart: {chart_file.name}")
        plt.close()

        # Save summary table
        impact_summary = self.impact_df.groupby(['year_numeric', 'impact_area'])['occurrence_count'].sum().unstack(fill_value=0)
        table_file = self.tables_dir / 'impact_areas_by_year.csv'
        impact_summary.to_csv(table_file)
        print(f"✓ Saved table: {table_file.name}")

    def create_overall_dashboard(self):
        """Create comprehensive dashboard visualization"""
        print("\n" + "="*80)
        print("CREATING COMPREHENSIVE DASHBOARD")
        print("="*80)

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Targets by Year
        if not self.targets_df.empty:
            ax1 = fig.add_subplot(gs[0, 0])
            targets_by_year = self.targets_df['year_numeric'].value_counts().sort_index()
            ax1.bar(targets_by_year.index, targets_by_year.values, color='steelblue', alpha=0.8)
            ax1.set_title('ESG Targets & Goals Mentions', fontweight='bold')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Count')
            ax1.grid(axis='y', alpha=0.3)

        # 2. Commitment Language Distribution
        if not self.language_df.empty:
            ax2 = fig.add_subplot(gs[0, 1])
            commitment_counts = self.language_df['commitment_strength'].value_counts()
            colors_pie = ['#2E7D32', '#FFA726', '#D32F2F']
            ax2.pie(commitment_counts.values, labels=commitment_counts.index, autopct='%1.1f%%',
                   colors=colors_pie, startangle=90)
            ax2.set_title('Commitment Language Distribution', fontweight='bold')

        # 3. Initiatives Over Time
        if not self.initiatives_df.empty:
            ax3 = fig.add_subplot(gs[1, 0])
            initiatives_by_year = self.initiatives_df['year_numeric'].value_counts().sort_index()
            ax3.plot(initiatives_by_year.index, initiatives_by_year.values, marker='o', linewidth=2, color='#1976D2')
            ax3.set_title('Initiative Announcements', fontweight='bold')
            ax3.set_xlabel('Year')
            ax3.set_ylabel('Count')
            ax3.grid(alpha=0.3)

        # 4. Top Impact Areas
        if not self.impact_df.empty:
            ax4 = fig.add_subplot(gs[1, 1])
            top_impact = self.impact_df.groupby('impact_area')['occurrence_count'].sum().nlargest(8).sort_values()
            ax4.barh(range(len(top_impact)), top_impact.values, color='coral', alpha=0.8)
            ax4.set_yticks(range(len(top_impact)))
            ax4.set_yticklabels(top_impact.index, fontsize=9)
            ax4.set_title('Top 8 Impact Areas by Mentions', fontweight='bold')
            ax4.set_xlabel('Total Mentions')
            ax4.grid(axis='x', alpha=0.3)

        # 5. Document Type Distribution
        if not self.targets_df.empty:
            ax5 = fig.add_subplot(gs[2, :])
            doc_type_counts = self.targets_df['document'].value_counts()
            ax5.barh(range(len(doc_type_counts)), doc_type_counts.values, color='mediumpurple', alpha=0.8)
            ax5.set_yticks(range(len(doc_type_counts)))
            ax5.set_yticklabels(doc_type_counts.index, fontsize=9)
            ax5.set_title('Target/Goal Mentions by Document Type', fontweight='bold')
            ax5.set_xlabel('Count')
            ax5.grid(axis='x', alpha=0.3)

        fig.suptitle('Ralph Lauren ESG Corporate Response Analysis - Dashboard', fontsize=16, fontweight='bold', y=0.995)

        chart_file = self.charts_dir / 'comprehensive_dashboard.png'
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved comprehensive dashboard: {chart_file.name}")
        plt.close()

    def create_summary_report(self):
        """Create text summary report of key findings"""
        print("\n" + "="*80)
        print("CREATING SUMMARY REPORT")
        print("="*80)

        report_file = self.output_dir / 'analysis_summary_report.txt'

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RALPH LAUREN ESG CORPORATE RESPONSE ANALYSIS\n")
            f.write("QUANTITATIVE ANALYSIS SUMMARY REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Key Metrics
            f.write("KEY METRICS:\n")
            f.write("-"*80 + "\n")
            f.write(f"Total Target/Goal Mentions Extracted: {len(self.targets_df)}\n")
            f.write(f"Total Language Patterns Identified: {len(self.language_df)}\n")
            f.write(f"Total Initiative References: {len(self.initiatives_df)}\n")
            f.write(f"Total Impact Area Mentions: {len(self.impact_df)}\n\n")

            # Year-over-Year Analysis
            if not self.targets_df.empty:
                f.write("TARGETS & GOALS - YEAR-OVER-YEAR:\n")
                f.write("-"*80 + "\n")
                targets_by_year = self.targets_df['year_numeric'].value_counts().sort_index()
                for year, count in targets_by_year.items():
                    f.write(f"  {int(year)}: {count} mentions\n")
                f.write("\n")

            # Language Strength Analysis
            if not self.language_df.empty:
                f.write("COMMITMENT LANGUAGE STRENGTH:\n")
                f.write("-"*80 + "\n")
                strength_counts = self.language_df['commitment_strength'].value_counts()
                total_language = len(self.language_df)
                for strength, count in strength_counts.items():
                    pct = (count / total_language) * 100
                    f.write(f"  {strength}: {count} ({pct:.1f}%)\n")
                f.write("\n")

            # Top Impact Areas
            if not self.impact_df.empty:
                f.write("TOP 10 IMPACT AREAS BY MENTION FREQUENCY:\n")
                f.write("-"*80 + "\n")
                top_impact = self.impact_df.groupby('impact_area')['occurrence_count'].sum().nlargest(10)
                for i, (area, count) in enumerate(top_impact.items(), 1):
                    f.write(f"  {i}. {area}: {int(count)} mentions\n")
                f.write("\n")

            # Document Type Analysis
            if not self.targets_df.empty:
                f.write("TARGETS BY DOCUMENT TYPE:\n")
                f.write("-"*80 + "\n")
                doc_counts = self.targets_df['document'].value_counts()
                for doc_type, count in doc_counts.items():
                    f.write(f"  {doc_type}: {count}\n")
                f.write("\n")

            f.write("="*80 + "\n")
            f.write("END OF SUMMARY REPORT\n")
            f.write("="*80 + "\n")

        print(f"✓ Saved summary report: {report_file.name}")

    def run_all_analyses(self):
        """Execute all analysis and visualization functions"""
        print(f"\n{'='*80}")
        print("RALPH LAUREN ESG ANALYSIS - QUANTITATIVE ANALYSIS & VISUALIZATION")
        print(f"{'='*80}")

        self.analyze_targets_over_time()
        self.analyze_commitment_language()
        self.analyze_initiatives()
        self.analyze_impact_areas()
        self.create_overall_dashboard()
        self.create_summary_report()

        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"\nAll outputs saved to:")
        print(f"  Charts: {self.charts_dir}")
        print(f"  Tables: {self.tables_dir}")
        print(f"  Summary: {self.output_dir / 'analysis_summary_report.txt'}\n")


def main():
    """Main execution function"""
    data_dir = Path(__file__).parent / 'structured_data_output'
    output_dir = Path(__file__).parent / 'analysis_output'

    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        print("Please run 03_esg_data_extractor.py first.")
        return

    analyzer = ESGAnalyzer(data_dir, output_dir)
    analyzer.run_all_analyses()


if __name__ == "__main__":
    main()

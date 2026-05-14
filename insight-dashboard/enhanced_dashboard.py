"""
========================================
ENHANCED EXCEL DASHBOARD GENERATOR
========================================
This script processes customer insights, derives features using AI analysis,
and generates a comprehensive Excel dashboard with:

1. Cluster Overview - Insights, Features, Companies per cluster
2. Year-wise Trends - Cluster importance over time
3. Feature Ranking - RICE scores at feature level
4. Feature Details - Insights mapped to features
5. Sample Quotes - Customer voice per feature

Usage:
    python enhanced_dashboard.py <input_file> [output_file] [--tag-filter=TAG]
"""

import pandas as pd
import sys
from datetime import datetime
from pathlib import Path

# Import our modules
from config import CLUSTER_DEFINITIONS
from data_processor import load_data, prepare_insights
from classifier import classify_all_insights
from feature_extractor import (
    group_insights_into_features, 
    get_cluster_summary,
    get_year_trend_data
)
from feature_rice_scorer import score_features

try:
    import xlsxwriter
    USE_XLSXWRITER = True
except ImportError:
    USE_XLSXWRITER = False


def create_enhanced_dashboard(classified_df, features_df, cluster_summary, 
                               year_trend, output_path):
    """Create the enhanced Excel dashboard with feature-level analysis."""
    
    workbook = xlsxwriter.Workbook(output_path)
    
    # =========================================================================
    # DEFINE FORMATS
    # =========================================================================
    title_format = workbook.add_format({
        'bold': True, 'font_size': 24, 'font_color': '#0070F2',
        'align': 'center', 'valign': 'vcenter'
    })
    subtitle_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'font_color': '#333333',
        'align': 'left', 'valign': 'vcenter'
    })
    header_format = workbook.add_format({
        'bold': True, 'font_size': 11, 'bg_color': '#0070F2', 
        'font_color': 'white', 'align': 'center', 'valign': 'vcenter',
        'border': 1, 'text_wrap': True
    })
    section_format = workbook.add_format({
        'bold': True, 'font_size': 14, 'font_color': '#0070F2',
        'bottom': 2, 'bottom_color': '#0070F2'
    })
    metric_label_format = workbook.add_format({
        'bold': True, 'font_size': 11, 'align': 'center', 
        'valign': 'vcenter', 'bg_color': '#E8E8E8', 'border': 1
    })
    metric_value_format = workbook.add_format({
        'bold': True, 'font_size': 20, 'font_color': '#0070F2',
        'align': 'center', 'valign': 'vcenter'
    })
    cell_format = workbook.add_format({
        'align': 'left', 'valign': 'vcenter', 'border': 1, 'text_wrap': True
    })
    center_cell = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1
    })
    number_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0'
    })
    percent_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '0.0%'
    })
    rice_high_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1,
        'bg_color': '#90EE90', 'bold': True, 'num_format': '0.00'
    })
    rice_medium_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1,
        'bg_color': '#FFFFE0', 'bold': True, 'num_format': '0.00'
    })
    rice_low_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'border': 1,
        'bg_color': '#FFB6C1', 'bold': True, 'num_format': '0.00'
    })
    quote_format = workbook.add_format({
        'italic': True, 'text_wrap': True, 'valign': 'top',
        'font_color': '#555555', 'border': 1, 'font_size': 10
    })
    cluster_header_format = workbook.add_format({
        'bold': True, 'font_size': 12, 'bg_color': '#1A9898', 
        'font_color': 'white', 'align': 'center', 'valign': 'vcenter',
        'border': 1
    })
    
    # =========================================================================
    # SHEET 1: DASHBOARD OVERVIEW
    # =========================================================================
    dashboard = workbook.add_worksheet('Dashboard')
    dashboard.set_column('A:A', 3)
    dashboard.set_column('B:B', 35)
    dashboard.set_column('C:H', 15)
    dashboard.set_column('I:I', 3)
    
    # Title
    dashboard.merge_range('B2:H2', '🎯 Insight Intelligence Dashboard - Feature Analysis', title_format)
    dashboard.set_row(1, 40)
    dashboard.write('B3', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | Process Governance Focus')
    
    # Key Metrics
    row = 5
    dashboard.write(f'B{row}', 'KEY METRICS', section_format)
    row += 2
    
    total_insights = len(classified_df)
    total_features = len(features_df)
    unique_companies = classified_df['cleaned_company'].nunique()
    total_clusters = classified_df['cluster'].nunique()
    avg_insights_per_feature = round(total_insights / max(total_features, 1), 1)
    top_rice = features_df['rice_score'].max() if len(features_df) > 0 else 0
    
    metrics = [
        ('Total Insights', f'{total_insights:,}'),
        ('Features Derived', f'{total_features:,}'),
        ('Companies Impacted', f'{unique_companies:,}'),
        ('Clusters', str(total_clusters)),
        ('Avg Insights/Feature', f'{avg_insights_per_feature}'),
        ('Top RICE Score', f'{top_rice:.1f}')
    ]
    
    col = 1  # Column B
    for label, value in metrics:
        dashboard.write(row, col, label, metric_label_format)
        dashboard.write(row + 1, col, value, metric_value_format)
        col += 1
    
    row += 4
    
    # Cluster Summary Table
    dashboard.write(f'B{row}', 'CLUSTER SUMMARY', section_format)
    row += 2
    
    headers = ['Cluster', 'Insights', 'Features', 'Companies', 'Insights/Feature']
    for col, header in enumerate(headers):
        dashboard.write(row - 1, col + 1, header, header_format)
    
    chart_data_start_row = row
    
    # Sort clusters by insight count
    cluster_summary_sorted = cluster_summary.sort_values('total_insights', ascending=False)
    
    for _, cs in cluster_summary_sorted.iterrows():
        dashboard.write(row, 1, cs['cluster'], cell_format)
        dashboard.write(row, 2, int(cs['total_insights']), number_format)
        dashboard.write(row, 3, int(cs['total_features']), number_format)
        dashboard.write(row, 4, int(cs['total_companies']), number_format)
        dashboard.write(row, 5, cs['avg_insights_per_feature'], center_cell)
        row += 1
    
    chart_data_end_row = row - 1
    
    # Create pie chart for insights distribution
    pie_chart = workbook.add_chart({'type': 'pie'})
    pie_chart.add_series({
        'name': 'Insights by Cluster',
        'categories': f'=Dashboard!$B${chart_data_start_row}:$B${chart_data_end_row}',
        'values': f'=Dashboard!$C${chart_data_start_row}:$C${chart_data_end_row}',
        'data_labels': {'percentage': True, 'category': False},
    })
    pie_chart.set_title({'name': 'Insights Distribution'})
    pie_chart.set_style(10)
    pie_chart.set_size({'width': 380, 'height': 280})
    dashboard.insert_chart(f'G{chart_data_start_row - 1}', pie_chart)
    
    row += 2
    
    # =========================================================================
    # SHEET 2: YEAR-WISE TRENDS
    # =========================================================================
    trends = workbook.add_worksheet('Year Trends')
    trends.set_column('A:A', 3)
    trends.set_column('B:B', 35)
    trends.set_column('C:L', 12)
    
    trends.merge_range('B2:K2', '📈 Year-wise Trend Analysis', title_format)
    trends.set_row(1, 40)
    
    # Get unique years
    if len(year_trend) > 0:
        years = sorted(year_trend['year'].dropna().unique())
        years = [y for y in years if pd.notna(y) and y > 2015]  # Filter valid years
    else:
        years = []
    
    row = 4
    trends.write(f'B{row}', 'INSIGHT TRENDS BY CLUSTER', section_format)
    row += 2
    
    # Headers
    trends.write(row - 1, 1, 'Cluster', header_format)
    for col, year in enumerate(years):
        trends.write(row - 1, col + 2, int(year), header_format)
    trends.write(row - 1, len(years) + 2, 'Total', header_format)
    
    trend_data_start_row = row
    
    # Data rows per cluster
    clusters = classified_df['cluster'].unique()
    for cluster in sorted(clusters):
        cluster_trend = year_trend[year_trend['cluster'] == cluster]
        
        trends.write(row, 1, cluster, cell_format)
        total = 0
        
        for col, year in enumerate(years):
            year_data = cluster_trend[cluster_trend['year'] == year]
            count = int(year_data['insight_count'].sum()) if len(year_data) > 0 else 0
            trends.write(row, col + 2, count, number_format)
            total += count
        
        trends.write(row, len(years) + 2, total, number_format)
        row += 1
    
    trend_data_end_row = row - 1
    
    # Create trend line chart
    if len(years) > 0:
        line_chart = workbook.add_chart({'type': 'line'})
        
        for i, cluster in enumerate(sorted(clusters)):
            line_chart.add_series({
                'name': f'=\'Year Trends\'!$B${trend_data_start_row + i}',
                'categories': f'=\'Year Trends\'!$C${trend_data_start_row - 1}:${chr(66 + len(years))}${trend_data_start_row - 1}',
                'values': f'=\'Year Trends\'!$C${trend_data_start_row + i}:${chr(66 + len(years))}${trend_data_start_row + i}',
                'marker': {'type': 'circle'},
            })
        
        line_chart.set_title({'name': 'Cluster Trends Over Time'})
        line_chart.set_x_axis({'name': 'Year'})
        line_chart.set_y_axis({'name': 'Number of Insights'})
        line_chart.set_size({'width': 700, 'height': 400})
        line_chart.set_legend({'position': 'bottom'})
        
        trends.insert_chart(f'B{row + 3}', line_chart)
    
    # =========================================================================
    # SHEET 3: FEATURE RANKING (RICE Scores)
    # =========================================================================
    ranking = workbook.add_worksheet('Feature Ranking')
    ranking.set_column('A:A', 6)
    ranking.set_column('B:B', 35)
    ranking.set_column('C:C', 30)
    ranking.set_column('D:D', 12)
    ranking.set_column('E:E', 12)
    ranking.set_column('F:F', 10)
    ranking.set_column('G:J', 10)
    ranking.set_column('K:K', 12)
    
    ranking.merge_range('A1:K1', '🏆 Feature Ranking by RICE Score', title_format)
    ranking.set_row(0, 40)
    
    ranking.write('A2', 'Features are potential product enhancements derived from customer insights. RICE = (Reach × Impact × Confidence) / Effort')
    
    # Headers
    headers = ['Rank', 'Feature', 'Cluster', 'Insights', 'Companies', '% Reach', 
               'Impact', 'Confidence', 'Effort', 'RICE Score']
    for col, header in enumerate(headers):
        ranking.write(3, col, header, header_format)
    
    # Data rows (top 50 features)
    row = 4
    for _, feat in features_df.head(50).iterrows():
        ranking.write(row, 0, int(feat['rank']), center_cell)
        ranking.write(row, 1, feat['feature_name'], cell_format)
        ranking.write(row, 2, feat['cluster'], cell_format)
        ranking.write(row, 3, int(feat['insight_count']), number_format)
        ranking.write(row, 4, int(feat['company_count']), number_format)
        ranking.write(row, 5, feat['reach_pct'] / 100, percent_format)
        ranking.write(row, 6, feat['impact'], center_cell)
        ranking.write(row, 7, feat['confidence'], center_cell)
        ranking.write(row, 8, int(feat['effort']), center_cell)
        
        # Color code RICE score
        rice = feat['rice_score']
        if rice >= 5:
            rice_fmt = rice_high_format
        elif rice >= 2:
            rice_fmt = rice_medium_format
        else:
            rice_fmt = rice_low_format
        ranking.write(row, 9, rice, rice_fmt)
        row += 1
    
    # Create RICE chart for top 15 features
    rice_chart = workbook.add_chart({'type': 'bar'})
    rice_chart.add_series({
        'name': 'RICE Score',
        'categories': f'=\'Feature Ranking\'!$B$5:$B${min(19, row)}',
        'values': f'=\'Feature Ranking\'!$J$5:$J${min(19, row)}',
        'fill': {'color': '#0070F2'},
        'data_labels': {'value': True, 'num_format': '0.0'},
    })
    rice_chart.set_title({'name': 'Top Features by RICE Score'})
    rice_chart.set_size({'width': 500, 'height': 400})
    rice_chart.set_legend({'none': True})
    rice_chart.set_y_axis({'reverse': True})
    ranking.insert_chart('L4', rice_chart)
    
    # =========================================================================
    # SHEET 4: FEATURE DETAILS WITH QUOTES
    # =========================================================================
    details = workbook.add_worksheet('Feature Details')
    details.set_column('A:A', 6)
    details.set_column('B:B', 30)
    details.set_column('C:C', 25)
    details.set_column('D:D', 10)
    details.set_column('E:E', 10)
    details.set_column('F:F', 10)
    details.set_column('G:G', 70)
    details.set_column('H:H', 25)
    
    details.merge_range('A1:H1', '📋 Feature Details with Customer Quotes', title_format)
    details.set_row(0, 40)
    
    headers = ['Rank', 'Feature', 'Cluster', 'Insights', 'Companies', 'RICE', 'Sample Quote', 'Company']
    for col, header in enumerate(headers):
        details.write(2, col, header, header_format)
    
    row = 3
    for _, feat in features_df.head(100).iterrows():
        quotes = feat.get('sample_quotes', [])
        companies = feat.get('companies', [])
        
        # Write first row with feature info
        details.write(row, 0, int(feat['rank']), center_cell)
        details.write(row, 1, feat['feature_name'], cell_format)
        details.write(row, 2, feat['cluster'], cell_format)
        details.write(row, 3, int(feat['insight_count']), number_format)
        details.write(row, 4, int(feat['company_count']), number_format)
        
        rice = feat['rice_score']
        if rice >= 5:
            rice_fmt = rice_high_format
        elif rice >= 2:
            rice_fmt = rice_medium_format
        else:
            rice_fmt = rice_low_format
        details.write(row, 5, rice, rice_fmt)
        
        # First quote
        if quotes:
            quote = str(quotes[0])[:400] + ('...' if len(str(quotes[0])) > 400 else '')
            details.write(row, 6, quote, quote_format)
            details.write(row, 7, companies[0] if companies else '', cell_format)
            details.set_row(row, 60)  # Taller row for quotes
        
        row += 1
        
        # Additional quotes (up to 2 more)
        for i in range(1, min(3, len(quotes))):
            quote = str(quotes[i])[:400] + ('...' if len(str(quotes[i])) > 400 else '')
            details.write(row, 6, quote, quote_format)
            details.write(row, 7, companies[i] if i < len(companies) else '', cell_format)
            details.set_row(row, 50)
            row += 1
    
    # =========================================================================
    # SHEET 5: CLUSTER → FEATURE MAPPING
    # =========================================================================
    mapping = workbook.add_worksheet('Cluster Features')
    mapping.set_column('A:A', 30)
    mapping.set_column('B:B', 35)
    mapping.set_column('C:C', 10)
    mapping.set_column('D:D', 10)
    mapping.set_column('E:E', 10)
    
    mapping.merge_range('A1:E1', '🗂️ Features by Cluster', title_format)
    mapping.set_row(0, 40)
    
    headers = ['Cluster', 'Feature', 'Insights', 'Companies', 'RICE']
    for col, header in enumerate(headers):
        mapping.write(2, col, header, header_format)
    
    row = 3
    current_cluster = None
    
    # Sort by cluster then by RICE score
    sorted_features = features_df.sort_values(['cluster', 'rice_score'], ascending=[True, False])
    
    for _, feat in sorted_features.iterrows():
        # Add cluster header row when cluster changes
        if feat['cluster'] != current_cluster:
            if current_cluster is not None:
                row += 1  # Add spacing
            current_cluster = feat['cluster']
            
            # Get cluster totals
            cluster_feats = features_df[features_df['cluster'] == current_cluster]
            cluster_insights = cluster_feats['insight_count'].sum()
            cluster_companies = cluster_feats['company_count'].max()  # Approximate
            
            mapping.merge_range(row, 0, row, 4, 
                f'{current_cluster} ({len(cluster_feats)} features, {cluster_insights} insights)',
                cluster_header_format)
            row += 1
        
        # Feature row
        mapping.write(row, 0, '', cell_format)
        mapping.write(row, 1, feat['feature_name'], cell_format)
        mapping.write(row, 2, int(feat['insight_count']), number_format)
        mapping.write(row, 3, int(feat['company_count']), number_format)
        
        rice = feat['rice_score']
        if rice >= 5:
            rice_fmt = rice_high_format
        elif rice >= 2:
            rice_fmt = rice_medium_format
        else:
            rice_fmt = rice_low_format
        mapping.write(row, 4, rice, rice_fmt)
        row += 1
    
    # =========================================================================
    # SHEET 6: RICE BREAKDOWN
    # =========================================================================
    rice_sheet = workbook.add_worksheet('RICE Breakdown')
    rice_sheet.set_column('A:A', 35)
    rice_sheet.set_column('B:B', 25)
    rice_sheet.set_column('C:G', 12)
    
    rice_sheet.merge_range('A1:G1', '📊 RICE Score Components', title_format)
    rice_sheet.set_row(0, 40)
    
    rice_sheet.write('A2', 'RICE = (Reach × Impact × Confidence) / Effort  |  Higher score = Higher priority')
    
    headers = ['Feature', 'Cluster', 'Reach', 'Impact', 'Confidence', 'Effort', 'RICE Score']
    for col, header in enumerate(headers):
        rice_sheet.write(3, col, header, header_format)
    
    row = 4
    for _, feat in features_df.head(50).iterrows():
        rice_sheet.write(row, 0, feat['feature_name'], cell_format)
        rice_sheet.write(row, 1, feat['cluster'], cell_format)
        rice_sheet.write(row, 2, int(feat['reach']), number_format)
        rice_sheet.write(row, 3, feat['impact'], center_cell)
        rice_sheet.write(row, 4, feat['confidence'], center_cell)
        rice_sheet.write(row, 5, int(feat['effort']), center_cell)
        
        rice = feat['rice_score']
        if rice >= 5:
            rice_fmt = rice_high_format
        elif rice >= 2:
            rice_fmt = rice_medium_format
        else:
            rice_fmt = rice_low_format
        rice_sheet.write(row, 6, rice, rice_fmt)
        row += 1
    
    # Legend
    row += 2
    rice_sheet.write(row, 0, 'RICE Components Explained:', section_format)
    row += 2
    explanations = [
        ('Reach', 'Number of unique companies requesting this feature'),
        ('Impact', 'Severity/importance (0.5=low to 3.0=critical) based on language used'),
        ('Confidence', 'Data confidence (0-1.0) based on number of supporting insights'),
        ('Effort', 'Estimated complexity (1-10, higher = more effort)'),
        ('RICE Score', 'Priority score. Higher = more valuable and higher priority'),
    ]
    for component, description in explanations:
        rice_sheet.write(row, 0, component, metric_label_format)
        rice_sheet.write(row, 1, description, cell_format)
        rice_sheet.merge_range(row, 1, row, 4, description, cell_format)
        row += 1
    
    # =========================================================================
    # SHEET 7: ALL CLASSIFIED DATA
    # =========================================================================
    raw_data = workbook.add_worksheet('All Insights')
    
    export_cols = ['insight_id', 'cluster', 'subcluster', 'cleaned_text', 
                   'cleaned_company', 'overall_confidence']
    
    # Add date columns if available
    for date_col in ['created_at', 'date']:
        if date_col in classified_df.columns:
            export_cols.append(date_col)
    
    export_cols = [c for c in export_cols if c in classified_df.columns]
    
    # Headers
    for col, header in enumerate(export_cols):
        raw_data.write(0, col, header, header_format)
    
    # Data
    for row_idx, (_, data_row) in enumerate(classified_df[export_cols].iterrows(), start=1):
        for col_idx, value in enumerate(data_row):
            if pd.isna(value):
                raw_data.write(row_idx, col_idx, '')
            else:
                raw_data.write(row_idx, col_idx, str(value)[:500])
    
    # Auto-filter
    raw_data.autofilter(0, 0, len(classified_df), len(export_cols) - 1)
    
    # Set column widths
    raw_data.set_column('A:A', 10)
    raw_data.set_column('B:C', 25)
    raw_data.set_column('D:D', 60)
    raw_data.set_column('E:E', 25)
    raw_data.set_column('F:G', 15)
    
    workbook.close()
    print(f"\n✅ Enhanced dashboard created: {output_path}")


def generate_enhanced_dashboard(input_file: str, output_file: str = None, 
                                 tag_filter: str = None):
    """
    Main function to generate the enhanced Excel dashboard.
    """
    print("=" * 70)
    print("🎯 Enhanced Insight Intelligence Dashboard - Feature Analysis")
    print("=" * 70)
    
    # Determine output path
    if output_file is None:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"feature_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    
    # Step 1: Load data
    print("\n📁 Loading data...")
    raw_df = load_data(input_file)
    
    # Step 1b: Filter by tag if specified
    if tag_filter:
        print(f"\n🏷️ Filtering for tag: '{tag_filter}'...")
        if 'tags' in raw_df.columns:
            original_count = len(raw_df)
            raw_df = raw_df[raw_df['tags'].str.contains(tag_filter, na=False, case=False)]
            print(f"   Filtered from {original_count:,} to {len(raw_df):,} insights")
        else:
            print("   ⚠️ No 'tags' column found, skipping filter")
    
    # Step 2: Prepare data
    print("\n🔄 Preparing insights...")
    prepared_df = prepare_insights(raw_df)
    
    # Step 3: Classify insights into clusters
    print("\n🤖 Classifying insights into clusters...")
    classified_df = classify_all_insights(prepared_df)
    
    # Step 4: Extract features from insights
    print("\n🔬 Deriving features from insights...")
    features_raw = group_insights_into_features(classified_df)
    
    # Step 5: Calculate RICE scores for features
    total_companies = classified_df['cleaned_company'].nunique()
    features_df = score_features(features_raw, total_companies)
    
    # Step 6: Generate cluster summary
    print("\n📊 Generating cluster summary...")
    cluster_summary = get_cluster_summary(classified_df, features_raw)
    
    # Step 7: Get year trend data
    print("\n📈 Analyzing year-wise trends...")
    year_trend = get_year_trend_data(classified_df)
    
    # Step 8: Create Excel dashboard
    print("\n📈 Creating enhanced Excel dashboard...")
    create_enhanced_dashboard(classified_df, features_df, cluster_summary, 
                               year_trend, output_file)
    
    print(f"\n✅ Dashboard generation complete!")
    print(f"📄 Output file: {output_file}")
    print("\n📋 Sheets included:")
    print("   1. Dashboard - Key metrics and cluster overview")
    print("   2. Year Trends - Cluster importance over time")
    print("   3. Feature Ranking - Top features by RICE score")
    print("   4. Feature Details - Features with customer quotes")
    print("   5. Cluster Features - Features organized by cluster")
    print("   6. RICE Breakdown - Detailed scoring components")
    print("   7. All Insights - Complete classified data")
    
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced_dashboard.py <input_file> [output_file] [--tag-filter=TAG]")
        print("\nExample:")
        print("  python enhanced_dashboard.py insights.xlsx")
        print('  python enhanced_dashboard.py insights.csv output.xlsx --tag-filter="Process Governance"')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = None
    tag_filter = None
    
    # Parse arguments
    for arg in sys.argv[2:]:
        if arg.startswith("--tag-filter="):
            tag_filter = arg.split("=", 1)[1].strip('"').strip("'")
        elif not arg.startswith("--"):
            output_file = arg
    
    generate_enhanced_dashboard(input_file, output_file, tag_filter)

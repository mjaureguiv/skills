"""
========================================
MULTI-PRODUCT DASHBOARD GENERATOR
========================================
Creates a comprehensive Excel dashboard with:
- One sheet per SAP Signavio product
- Themes/clusters dynamically identified per product
- Service tickets separated per product
- Year-wise trends and company distributions
- Cumulative overview dashboard

Usage:
    python multi_product_dashboard.py <input_file> [output_file]
"""

import pandas as pd
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Import our modules
from data_processor import load_data, prepare_insights
from product_classifier import (
    classify_all_insights_to_products, 
    get_product_list,
    get_product_description,
    get_product_capabilities
)
from dynamic_cluster_analyzer import (
    analyze_themes_for_product,
    derive_features_from_themes
)

try:
    import xlsxwriter
except ImportError:
    print("ERROR: xlsxwriter required. Install with: pip install xlsxwriter")
    sys.exit(1)


# ============================================================================
# EXCEL FORMATTING HELPERS
# ============================================================================

def get_formats(workbook):
    """Create standard formats for the workbook."""
    return {
        'title': workbook.add_format({
            'bold': True, 'font_size': 20, 'font_color': '#0070F2',
            'align': 'center', 'valign': 'vcenter'
        }),
        'subtitle': workbook.add_format({
            'bold': True, 'font_size': 14, 'font_color': '#333333'
        }),
        'section': workbook.add_format({
            'bold': True, 'font_size': 14, 'font_color': '#0070F2',
            'bottom': 2, 'bottom_color': '#0070F2'
        }),
        'header': workbook.add_format({
            'bold': True, 'font_size': 11, 'bg_color': '#0070F2',
            'font_color': 'white', 'align': 'center', 'valign': 'vcenter',
            'border': 1, 'text_wrap': True
        }),
        'header_dark': workbook.add_format({
            'bold': True, 'font_size': 12, 'bg_color': '#1A4D7C',
            'font_color': 'white', 'align': 'center', 'valign': 'vcenter',
            'border': 1
        }),
        'metric_label': workbook.add_format({
            'bold': True, 'font_size': 10, 'align': 'center',
            'bg_color': '#E8E8E8', 'border': 1
        }),
        'metric_value': workbook.add_format({
            'bold': True, 'font_size': 18, 'font_color': '#0070F2',
            'align': 'center', 'valign': 'vcenter'
        }),
        'cell': workbook.add_format({
            'align': 'left', 'valign': 'vcenter', 'border': 1, 'text_wrap': True
        }),
        'center': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1
        }),
        'number': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0'
        }),
        'percent': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '0.0%'
        }),
        'rice_high': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'bg_color': '#90EE90', 'bold': True, 'num_format': '0.00'
        }),
        'rice_mid': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'bg_color': '#FFFFE0', 'bold': True, 'num_format': '0.00'
        }),
        'rice_low': workbook.add_format({
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'bg_color': '#FFB6C1', 'bold': True, 'num_format': '0.00'
        }),
        'quote': workbook.add_format({
            'italic': True, 'text_wrap': True, 'valign': 'top',
            'font_color': '#555555', 'border': 1, 'font_size': 10
        }),
        'service_ticket': workbook.add_format({
            'bg_color': '#FFF3CD', 'border': 1, 'text_wrap': True
        })
    }


def truncate_sheet_name(name: str, max_len: int = 31) -> str:
    """Truncate sheet name to Excel's 31 character limit."""
    if len(name) <= max_len:
        return name
    return name[:max_len-3] + "..."


# ============================================================================
# PRODUCT SHEET GENERATOR
# ============================================================================

def create_product_sheet(workbook, product: str, product_df: pd.DataFrame, 
                          theme_analysis: Dict, features_df: pd.DataFrame,
                          formats: Dict):
    """
    Create a dashboard sheet for a single product.
    """
    sheet_name = truncate_sheet_name(product)
    sheet = workbook.add_worksheet(sheet_name)
    
    # Column widths
    sheet.set_column('A:A', 3)
    sheet.set_column('B:B', 30)
    sheet.set_column('C:C', 25)
    sheet.set_column('D:G', 12)
    sheet.set_column('H:H', 50)
    
    # Get data
    total_insights = len(product_df)
    text_col = 'cleaned_text' if 'cleaned_text' in product_df.columns else 'note_text'
    unique_companies = product_df['cleaned_company'].nunique() if 'cleaned_company' in product_df.columns else 0
    service_tickets = product_df[product_df['is_service_ticket'] == True] if 'is_service_ticket' in product_df.columns else pd.DataFrame()
    
    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    row = 1
    sheet.merge_range(f'B{row}:G{row}', f'📊 {product}', formats['title'])
    sheet.set_row(row - 1, 35)
    
    row += 1
    description = get_product_description(product)
    if description:
        sheet.write(f'B{row}', description)
    
    row += 2
    
    # -------------------------------------------------------------------------
    # KEY METRICS
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'KEY METRICS', formats['section'])
    row += 2
    
    theme_count = len(theme_analysis.get('themes', []))
    feature_count = len(features_df)
    ticket_count = len(service_tickets)
    
    metrics = [
        ('Total Insights', f'{total_insights:,}'),
        ('Themes', str(theme_count)),
        ('Features', str(feature_count)),
        ('Companies', f'{unique_companies:,}'),
        ('Service Tickets', str(ticket_count))
    ]
    
    col = 1
    for label, value in metrics:
        sheet.write(row, col, label, formats['metric_label'])
        sheet.write(row + 1, col, value, formats['metric_value'])
        col += 1
    
    row += 4
    
    # -------------------------------------------------------------------------
    # THEME DISTRIBUTION
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'THEME DISTRIBUTION', formats['section'])
    row += 2
    
    headers = ['Theme', 'Insights', '% Share', 'Companies']
    for col, header in enumerate(headers):
        sheet.write(row - 1, col + 1, header, formats['header'])
    
    theme_data_start = row
    themes = theme_analysis.get('themes', [])
    
    for theme in themes[:15]:  # Top 15 themes
        sheet.write(row, 1, theme['theme'], formats['cell'])
        sheet.write(row, 2, theme['insight_count'], formats['number'])
        sheet.write(row, 3, theme['percentage'] / 100, formats['percent'])
        sheet.write(row, 4, theme['company_count'], formats['number'])
        row += 1
    
    theme_data_end = row - 1
    
    # Pie chart for theme distribution
    if themes:
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.add_series({
            'name': 'Theme Distribution',
            'categories': f"='{sheet_name}'!$B${theme_data_start}:$B${min(theme_data_start + 7, theme_data_end)}",
            'values': f"='{sheet_name}'!$C${theme_data_start}:$C${min(theme_data_start + 7, theme_data_end)}",
            'data_labels': {'percentage': True}
        })
        pie_chart.set_title({'name': 'Theme Distribution'})
        pie_chart.set_size({'width': 350, 'height': 250})
        sheet.insert_chart(f'F{theme_data_start - 1}', pie_chart)
    
    row += 2
    
    # -------------------------------------------------------------------------
    # YEAR-WISE TREND
    # -------------------------------------------------------------------------
    year_trend = theme_analysis.get('year_trend', pd.DataFrame())
    
    if len(year_trend) > 0:
        sheet.write(f'B{row}', 'YEAR-WISE TREND', formats['section'])
        row += 2
        
        # Aggregate by year
        if 'created_at' in product_df.columns:
            product_df_temp = product_df.copy()
            product_df_temp['year'] = pd.to_datetime(product_df_temp['created_at'], errors='coerce').dt.year
            year_counts = product_df_temp.groupby('year').size().reset_index(name='count')
            year_counts = year_counts[(year_counts['year'] > 2015) & (year_counts['year'].notna())]
            
            if len(year_counts) > 0:
                headers = ['Year', 'Insights']
                for col, header in enumerate(headers):
                    sheet.write(row - 1, col + 1, header, formats['header'])
                
                year_data_start = row
                for _, yr in year_counts.iterrows():
                    sheet.write(row, 1, int(yr['year']), formats['center'])
                    sheet.write(row, 2, int(yr['count']), formats['number'])
                    row += 1
                year_data_end = row - 1
                
                # Line chart
                if len(year_counts) > 1:
                    line_chart = workbook.add_chart({'type': 'line'})
                    line_chart.add_series({
                        'name': 'Insights Over Time',
                        'categories': f"='{sheet_name}'!$B${year_data_start}:$B${year_data_end}",
                        'values': f"='{sheet_name}'!$C${year_data_start}:$C${year_data_end}",
                        'marker': {'type': 'circle'}
                    })
                    line_chart.set_title({'name': 'Year-wise Trend'})
                    line_chart.set_size({'width': 400, 'height': 220})
                    sheet.insert_chart(f'E{year_data_start - 1}', line_chart)
        
        row += 2
    
    # -------------------------------------------------------------------------
    # TOP FEATURES
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'TOP FEATURES (Potential Enhancements)', formats['section'])
    row += 2
    
    headers = ['Rank', 'Feature', 'Theme', 'Insights', 'Companies', 'RICE']
    for col, header in enumerate(headers):
        sheet.write(row - 1, col + 1, header, formats['header'])
    
    for _, feat in features_df.head(15).iterrows():
        sheet.write(row, 1, int(feat.get('rank', 0)), formats['center'])
        sheet.write(row, 2, str(feat.get('feature_name', ''))[:60], formats['cell'])
        sheet.write(row, 3, str(feat.get('theme', '')), formats['cell'])
        sheet.write(row, 4, int(feat.get('insight_count', 0)), formats['number'])
        sheet.write(row, 5, int(feat.get('company_count', 0)), formats['number'])
        
        rice = feat.get('rice_score', 0)
        if rice >= 5:
            rice_fmt = formats['rice_high']
        elif rice >= 2:
            rice_fmt = formats['rice_mid']
        else:
            rice_fmt = formats['rice_low']
        sheet.write(row, 6, rice, rice_fmt)
        row += 1
    
    row += 2
    
    # -------------------------------------------------------------------------
    # COMPANY DISTRIBUTION
    # -------------------------------------------------------------------------
    company_dist = theme_analysis.get('company_dist', pd.DataFrame())
    
    if len(company_dist) > 0:
        sheet.write(f'B{row}', 'TOP COMPANIES', formats['section'])
        row += 2
        
        # Aggregate across all themes
        if 'cleaned_company' in product_df.columns:
            top_companies = product_df['cleaned_company'].value_counts().head(15)
            
            headers = ['Company', 'Insights']
            for col, header in enumerate(headers):
                sheet.write(row - 1, col + 1, header, formats['header'])
            
            for company, count in top_companies.items():
                if company and pd.notna(company):
                    sheet.write(row, 1, str(company), formats['cell'])
                    sheet.write(row, 2, int(count), formats['number'])
                    row += 1
        
        row += 2
    
    # -------------------------------------------------------------------------
    # SERVICE TICKETS SECTION
    # -------------------------------------------------------------------------
    if len(service_tickets) > 0:
        sheet.write(f'B{row}', f'SERVICE TICKETS ({len(service_tickets)})', formats['section'])
        row += 2
        
        headers = ['Company', 'Request']
        for col, header in enumerate(headers):
            sheet.write(row - 1, col + 1, header, formats['header'])
        
        for _, ticket in service_tickets.head(20).iterrows():
            company = ticket.get('cleaned_company', '') or ticket.get('company_name', '')
            text = str(ticket.get(text_col, ''))[:200]
            
            sheet.write(row, 1, str(company) if pd.notna(company) else '', formats['service_ticket'])
            sheet.write(row, 2, text, formats['service_ticket'])
            sheet.set_row(row, 40)
            row += 1


# ============================================================================
# CUMULATIVE DASHBOARD
# ============================================================================

def create_cumulative_dashboard(workbook, classified_df: pd.DataFrame, 
                                 product_summaries: Dict, formats: Dict):
    """
    Create the cumulative overview dashboard.
    """
    sheet = workbook.add_worksheet('Cumulative Overview')
    
    sheet.set_column('A:A', 3)
    sheet.set_column('B:B', 35)
    sheet.set_column('C:H', 15)
    
    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    row = 1
    sheet.merge_range(f'B{row}:H{row}', '🎯 SAP Signavio - Complete Insight Intelligence', formats['title'])
    sheet.set_row(row - 1, 40)
    
    row += 1
    sheet.write(f'B{row}', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} | All Products Analysis')
    row += 3
    
    # -------------------------------------------------------------------------
    # OVERALL METRICS
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'OVERALL METRICS', formats['section'])
    row += 2
    
    total_insights = len(classified_df)
    total_companies = classified_df['cleaned_company'].nunique() if 'cleaned_company' in classified_df.columns else 0
    total_products = len(product_summaries)
    total_service = classified_df['is_service_ticket'].sum() if 'is_service_ticket' in classified_df.columns else 0
    
    # Count total themes across all products
    total_themes = sum(len(s.get('themes', [])) for s in product_summaries.values())
    total_features = sum(len(s.get('features', [])) for s in product_summaries.values())
    
    metrics = [
        ('Total Insights', f'{total_insights:,}'),
        ('Products', str(total_products)),
        ('Total Companies', f'{total_companies:,}'),
        ('Themes Identified', str(total_themes)),
        ('Features Derived', str(total_features)),
        ('Service Tickets', f'{int(total_service):,}')
    ]
    
    col = 1
    for label, value in metrics:
        sheet.write(row, col, label, formats['metric_label'])
        sheet.write(row + 1, col, value, formats['metric_value'])
        col += 1
    
    row += 5
    
    # -------------------------------------------------------------------------
    # PRODUCT BREAKDOWN
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'INSIGHTS BY PRODUCT', formats['section'])
    row += 2
    
    headers = ['Product', 'Insights', '% Share', 'Companies', 'Themes', 'Service Tickets']
    for col, header in enumerate(headers):
        sheet.write(row - 1, col + 1, header, formats['header'])
    
    product_data_start = row
    
    # Sort products by insight count
    product_counts = classified_df['product'].value_counts()
    
    for product, count in product_counts.items():
        if product == 'Unclassified':
            continue
            
        product_df = classified_df[classified_df['product'] == product]
        pct = (count / total_insights) * 100
        companies = product_df['cleaned_company'].nunique() if 'cleaned_company' in product_df.columns else 0
        themes = len(product_summaries.get(product, {}).get('themes', []))
        tickets = product_df['is_service_ticket'].sum() if 'is_service_ticket' in product_df.columns else 0
        
        sheet.write(row, 1, product, formats['cell'])
        sheet.write(row, 2, int(count), formats['number'])
        sheet.write(row, 3, pct / 100, formats['percent'])
        sheet.write(row, 4, int(companies), formats['number'])
        sheet.write(row, 5, int(themes), formats['number'])
        sheet.write(row, 6, int(tickets), formats['number'])
        row += 1
    
    product_data_end = row - 1
    
    # Bar chart for product distribution
    bar_chart = workbook.add_chart({'type': 'bar'})
    bar_chart.add_series({
        'name': 'Insights by Product',
        'categories': f"='Cumulative Overview'!$B${product_data_start}:$B${product_data_end}",
        'values': f"='Cumulative Overview'!$C${product_data_start}:$C${product_data_end}",
        'fill': {'color': '#0070F2'},
        'data_labels': {'value': True, 'num_format': '#,##0'}
    })
    bar_chart.set_title({'name': 'Insights by Product'})
    bar_chart.set_size({'width': 500, 'height': 350})
    bar_chart.set_legend({'none': True})
    bar_chart.set_y_axis({'reverse': True})
    sheet.insert_chart(f'H{product_data_start - 1}', bar_chart)
    
    row += 3
    
    # -------------------------------------------------------------------------
    # YEAR-WISE OVERALL TREND
    # -------------------------------------------------------------------------
    if 'created_at' in classified_df.columns:
        sheet.write(f'B{row}', 'INSIGHTS OVER TIME', formats['section'])
        row += 2
        
        classified_df_temp = classified_df.copy()
        classified_df_temp['year'] = pd.to_datetime(classified_df_temp['created_at'], errors='coerce').dt.year
        year_counts = classified_df_temp.groupby('year').size().reset_index(name='count')
        year_counts = year_counts[(year_counts['year'] > 2015) & (year_counts['year'].notna())]
        
        if len(year_counts) > 0:
            headers = ['Year', 'Insights']
            for col, header in enumerate(headers):
                sheet.write(row - 1, col + 1, header, formats['header'])
            
            year_start = row
            for _, yr in year_counts.iterrows():
                sheet.write(row, 1, int(yr['year']), formats['center'])
                sheet.write(row, 2, int(yr['count']), formats['number'])
                row += 1
            year_end = row - 1
            
            # Line chart
            if len(year_counts) > 1:
                line_chart = workbook.add_chart({'type': 'line'})
                line_chart.add_series({
                    'name': 'Total Insights',
                    'categories': f"='Cumulative Overview'!$B${year_start}:$B${year_end}",
                    'values': f"='Cumulative Overview'!$C${year_start}:$C${year_end}",
                    'marker': {'type': 'circle', 'size': 8}
                })
                line_chart.set_title({'name': 'Insights Trend (All Products)'})
                line_chart.set_size({'width': 500, 'height': 280})
                sheet.insert_chart(f'E{year_start - 1}', line_chart)
        
        row += 2
    
    # -------------------------------------------------------------------------
    # TOP THEMES ACROSS ALL PRODUCTS
    # -------------------------------------------------------------------------
    sheet.write(f'B{row}', 'TOP THEMES ACROSS ALL PRODUCTS', formats['section'])
    row += 2
    
    # Aggregate themes from all products
    all_themes = {}
    for product, summary in product_summaries.items():
        for theme_data in summary.get('themes', []):
            theme = theme_data['theme']
            if theme not in all_themes:
                all_themes[theme] = {'insight_count': 0, 'company_count': 0, 'products': set()}
            all_themes[theme]['insight_count'] += theme_data['insight_count']
            all_themes[theme]['company_count'] = max(all_themes[theme]['company_count'], theme_data['company_count'])
            all_themes[theme]['products'].add(product)
    
    # Sort and display
    sorted_themes = sorted(all_themes.items(), key=lambda x: x[1]['insight_count'], reverse=True)
    
    headers = ['Theme', 'Insights', 'Products']
    for col, header in enumerate(headers):
        sheet.write(row - 1, col + 1, header, formats['header'])
    
    for theme, data in sorted_themes[:20]:
        sheet.write(row, 1, theme, formats['cell'])
        sheet.write(row, 2, data['insight_count'], formats['number'])
        sheet.write(row, 3, len(data['products']), formats['number'])
        row += 1
    
    row += 2
    
    # -------------------------------------------------------------------------
    # UNCLASSIFIED INSIGHTS
    # -------------------------------------------------------------------------
    unclassified = classified_df[classified_df['product'] == 'Unclassified']
    if len(unclassified) > 0:
        sheet.write(f'B{row}', f'UNCLASSIFIED INSIGHTS ({len(unclassified)})', formats['section'])
        row += 1
        sheet.write(f'B{row}', 'These insights could not be mapped to a specific product based on tags.')
        row += 2


# ============================================================================
# MAIN GENERATOR
# ============================================================================

def generate_multi_product_dashboard(input_file: str, output_file: str = None):
    """
    Generate the complete multi-product Excel dashboard.
    """
    print("=" * 70)
    print("🎯 SAP Signavio Multi-Product Dashboard Generator")
    print("=" * 70)
    
    # Determine output path
    if output_file is None:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"multi_product_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    
    # Step 1: Load and prepare data
    print("\n📁 Loading data...")
    raw_df = load_data(input_file)
    
    print("\n🔄 Preparing insights...")
    prepared_df = prepare_insights(raw_df)
    
    # Step 2: Classify to products
    print("\n🏷️ Classifying insights to SAP Signavio products...")
    classified_df = classify_all_insights_to_products(prepared_df)
    
    # Step 3: Analyze each product
    print("\n📊 Analyzing each product...")
    
    products = get_product_list()
    product_summaries = {}
    
    for product in products:
        product_df = classified_df[classified_df['product'] == product]
        
        if len(product_df) == 0:
            print(f"   ⚠️ {product}: No insights found")
            continue
        
        print(f"\n   📦 {product}: {len(product_df)} insights")
        
        # Analyze themes
        theme_analysis = analyze_themes_for_product(product_df, product)
        
        # Derive features
        df_with_themes = theme_analysis['df']
        features_df = derive_features_from_themes(df_with_themes)
        
        product_summaries[product] = {
            'df': product_df,
            'theme_analysis': theme_analysis,
            'features': features_df,
            'themes': theme_analysis.get('themes', [])
        }
    
    # Step 4: Create Excel workbook
    print("\n📈 Creating Excel dashboard...")
    
    workbook = xlsxwriter.Workbook(output_file)
    formats = get_formats(workbook)
    
    # Create cumulative overview first (appears as first sheet)
    create_cumulative_dashboard(workbook, classified_df, product_summaries, formats)
    
    # Create product sheets
    for product in products:
        if product not in product_summaries:
            continue
        
        summary = product_summaries[product]
        product_df = summary['df']
        theme_analysis = summary['theme_analysis']
        features_df = summary['features']
        
        print(f"   📄 Creating sheet: {product}")
        create_product_sheet(
            workbook, product, product_df, 
            theme_analysis, features_df, formats
        )
    
    # Add raw data sheet
    print("   📄 Creating All Insights sheet...")
    raw_sheet = workbook.add_worksheet('All Insights')
    
    export_cols = ['product', 'theme', 'is_service_ticket', 'cleaned_text', 
                   'cleaned_company', 'tags', 'created_at']
    export_cols = [c for c in export_cols if c in classified_df.columns]
    
    # Handle theme column from individual analyses
    if 'theme' not in classified_df.columns:
        # Combine themes from all product analyses
        all_themes = {}
        for product, summary in product_summaries.items():
            if 'df' in summary['theme_analysis']:
                theme_df = summary['theme_analysis']['df']
                if 'theme' in theme_df.columns:
                    for idx in theme_df.index:
                        all_themes[idx] = theme_df.loc[idx, 'theme']
        
        classified_df['theme'] = classified_df.index.map(lambda x: all_themes.get(x, 'Other'))
        export_cols = ['product', 'theme', 'is_service_ticket', 'cleaned_text', 
                       'cleaned_company', 'tags', 'created_at']
        export_cols = [c for c in export_cols if c in classified_df.columns]
    
    # Write headers
    for col, header in enumerate(export_cols):
        raw_sheet.write(0, col, header, formats['header'])
    
    # Write data
    for row_idx, (_, data_row) in enumerate(classified_df[export_cols].iterrows(), start=1):
        for col_idx, value in enumerate(data_row):
            if pd.isna(value):
                raw_sheet.write(row_idx, col_idx, '')
            elif isinstance(value, bool):
                raw_sheet.write(row_idx, col_idx, 'Yes' if value else 'No')
            else:
                raw_sheet.write(row_idx, col_idx, str(value)[:500])
    
    raw_sheet.autofilter(0, 0, len(classified_df), len(export_cols) - 1)
    raw_sheet.set_column('A:A', 25)
    raw_sheet.set_column('B:B', 20)
    raw_sheet.set_column('C:C', 12)
    raw_sheet.set_column('D:D', 60)
    raw_sheet.set_column('E:E', 25)
    raw_sheet.set_column('F:F', 30)
    raw_sheet.set_column('G:G', 18)
    
    workbook.close()
    
    # Summary
    print(f"\n✅ Dashboard generation complete!")
    print(f"📄 Output file: {output_file}")
    print("\n📋 Sheets included:")
    print("   1. Cumulative Overview - All products summary")
    
    sheet_num = 2
    for product in products:
        if product in product_summaries:
            summary = product_summaries[product]
            insight_count = len(summary['df'])
            print(f"   {sheet_num}. {product} ({insight_count} insights)")
            sheet_num += 1
    
    print(f"   {sheet_num}. All Insights - Complete classified data")
    
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multi_product_dashboard.py <input_file> [output_file]")
        print("\nExample:")
        print("  python multi_product_dashboard.py insights.csv")
        print("  python multi_product_dashboard.py insights.xlsx dashboard.xlsx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_multi_product_dashboard(input_file, output_file)

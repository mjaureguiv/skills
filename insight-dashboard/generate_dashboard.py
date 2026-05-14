#!/usr/bin/env python3
"""
========================================
PRODUCTBOARD INSIGHT DASHBOARD GENERATOR
========================================
Simple one-command tool to generate an actionable Excel dashboard
from ProductBoard customer insights.

USAGE:
    python generate_dashboard.py <input_file>
    python generate_dashboard.py <input_file> <output_file>

EXAMPLES:
    python generate_dashboard.py insights.csv
    python generate_dashboard.py insights.xlsx my_dashboard.xlsx
    python generate_dashboard.py ../../rawnotes/feedback.csv

The tool will:
1. Load your ProductBoard insights (CSV or Excel)
2. Clean and deduplicate the data
3. Classify insights by SAP Signavio product
4. Identify themes and patterns per product
5. Calculate RICE scores for prioritization
6. Generate a comprehensive Excel dashboard

OUTPUT:
    An Excel file with:
    - Cumulative Overview (all products summary)
    - Per-product sheets with themes, features, trends
    - All Insights raw data with filters
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the skill directory to path for imports
SKILL_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SKILL_DIR))


def print_banner():
    """Display a welcome banner."""
    print()
    print("=" * 60)
    print("  📊 ProductBoard Insight Dashboard Generator")
    print("=" * 60)
    print()


def print_usage():
    """Print usage instructions."""
    print("USAGE:")
    print("  python generate_dashboard.py <input_file> [output_file]")
    print()
    print("ARGUMENTS:")
    print("  input_file   - Path to CSV or Excel file with insights")
    print("  output_file  - (Optional) Path for output dashboard")
    print()
    print("EXAMPLES:")
    print("  python generate_dashboard.py insights.csv")
    print("  python generate_dashboard.py data.xlsx dashboard.xlsx")
    print()
    print("REQUIRED COLUMNS in your input file:")
    print("  - note_text      : The customer insight/feedback text")
    print("  - company_name   : The customer company name")
    print("  - tags           : (Optional) ProductBoard tags for classification")
    print("  - created_at     : (Optional) Date for trend analysis")
    print()


def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    try:
        import xlsxwriter
    except ImportError:
        missing.append("xlsxwriter")
    
    try:
        import openpyxl
    except ImportError:
        missing.append("openpyxl")
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print()
        print("Install them with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        print("Or install all dependencies:")
        print(f"   pip install -r {SKILL_DIR / 'requirements.txt'}")
        return False
    
    return True


def validate_input_file(input_file: str) -> Path:
    """Validate the input file exists and is readable."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        # Try relative to common locations
        alternatives = [
            Path(input_file),
            SKILL_DIR / input_file,
            SKILL_DIR.parent.parent / "rawnotes" / input_file,
            SKILL_DIR / "temp" / input_file,
        ]
        
        for alt in alternatives:
            if alt.exists():
                return alt.absolute()
        
        print(f"❌ File not found: {input_file}")
        print()
        print("Searched in:")
        for alt in alternatives:
            print(f"   - {alt}")
        sys.exit(1)
    
    # Validate file extension
    ext = input_path.suffix.lower()
    if ext not in ['.csv', '.xlsx', '.xls']:
        print(f"❌ Unsupported file type: {ext}")
        print("   Supported formats: .csv, .xlsx, .xls")
        sys.exit(1)
    
    return input_path.absolute()


def determine_output_path(input_path: Path, output_file: str = None) -> Path:
    """Determine the output file path."""
    if output_file:
        output_path = Path(output_file)
        if not output_path.suffix:
            output_path = output_path.with_suffix('.xlsx')
        return output_path.absolute()
    
    # Default: same directory as input with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_name = f"insight_dashboard_{timestamp}.xlsx"
    
    # Prefer outputs folder if it exists
    outputs_dir = SKILL_DIR.parent.parent / "outputs"
    if outputs_dir.exists():
        return (outputs_dir / output_name).absolute()
    
    # Otherwise use temp folder
    temp_dir = SKILL_DIR / "temp"
    temp_dir.mkdir(exist_ok=True)
    return (temp_dir / output_name).absolute()


def main():
    """Main entry point."""
    print_banner()
    
    # Parse arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    if sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Validate input
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    input_path = validate_input_file(input_file)
    output_path = determine_output_path(input_path, output_file)
    
    print(f"📁 Input:  {input_path}")
    print(f"📄 Output: {output_path}")
    print()
    
    # Import and run the dashboard generator
    try:
        from multi_product_dashboard import generate_multi_product_dashboard
        
        result = generate_multi_product_dashboard(
            str(input_path), 
            str(output_path)
        )
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! Your dashboard is ready.")
        print("=" * 60)
        print()
        print(f"📊 Open this file to view your dashboard:")
        print(f"   {result}")
        print()
        print("TIP: The Excel file contains multiple sheets:")
        print("   - 'Cumulative Overview' for high-level metrics")
        print("   - Product-specific sheets with detailed analysis")
        print("   - 'All Insights' for filtered data exploration")
        print()
        
        return result
        
    except Exception as e:
        print()
        print(f"❌ Error generating dashboard: {e}")
        print()
        print("Common issues:")
        print("  - Check that your file has 'note_text' column")
        print("  - Ensure file is not open in another program")
        print("  - Verify file is not corrupted")
        print()
        raise


if __name__ == "__main__":
    main()

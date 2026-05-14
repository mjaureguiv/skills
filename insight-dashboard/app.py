"""
========================================
CUSTOMER INSIGHT INTELLIGENCE DASHBOARD
========================================
This is the main Streamlit application that provides a visual interface
for exploring and analyzing customer insights.

How to Run:
    1. Open a terminal in this folder
    2. Run: streamlit run app.py
    3. Open your browser to http://localhost:8501

Dashboard Sections:
    1. Overview - Summary statistics and distribution charts
    2. Feature Ranking - Prioritized list with RICE scores
    3. Feature Details - Deep dive into specific features

Key Concepts for Beginners:
- Streamlit is a Python library that creates web apps easily
- We use st.xyz() functions to add elements to the page
- The app reruns whenever you interact with it
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

# Import our custom modules
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    CHART_COLORS,
    MAX_SAMPLE_QUOTES,
    DEFAULT_DATA_PATH,
    CLUSTER_DEFINITIONS,
)
from data_processor import load_data, prepare_insights, get_data_summary
from classifier import classify_all_insights, get_classification_summary
from rice_scorer import score_all_features, score_subfeatures, get_feature_details


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
# This must be the first Streamlit command

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM STYLING
# ============================================================================
# Add custom CSS to make the dashboard look nicer

st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0070F2;
        margin-bottom: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    /* Feature cards */
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0070F2;
        margin-bottom: 0.5rem;
    }
    
    /* Quote styling */
    .customer-quote {
        background: #f0f7ff;
        padding: 1rem;
        border-left: 3px solid #0070F2;
        margin: 0.5rem 0;
        font-style: italic;
    }
    
    /* RICE badge */
    .rice-badge {
        background: #0070F2;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
# Using Streamlit's caching to avoid reloading data on every interaction

@st.cache_data(show_spinner=False)
def load_and_process_data(file_path: str):
    """
    Load, clean, and classify all insights data.
    
    Uses caching so this only runs once (unless the file changes).
    
    Parameters:
        file_path: Path to the data file
    
    Returns:
        Tuple of (classified_df, features_df, subfeatures_df)
    """
    # Step 1: Load raw data
    raw_df = load_data(file_path)
    
    # Step 2: Clean and prepare
    prepared_df = prepare_insights(raw_df)
    
    # Step 3: Classify insights
    classified_df = classify_all_insights(prepared_df)
    
    # Step 4: Calculate RICE scores
    features_df = score_all_features(classified_df)
    subfeatures_df = score_subfeatures(classified_df)
    
    return classified_df, features_df, subfeatures_df


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render the sidebar with file upload and filters."""
    
    st.sidebar.title("🎯 Insight Dashboard")
    st.sidebar.markdown("---")
    
    # File selection
    st.sidebar.subheader("📁 Data Source")
    
    # Option 1: Use default file
    # Option 2: Upload new file
    data_source = st.sidebar.radio(
        "Select data source:",
        ["Use sample data", "Upload file"],
        index=0
    )
    
    file_path = None
    
    if data_source == "Use sample data":
        # Use the default path
        default_path = Path(__file__).parent / DEFAULT_DATA_PATH
        if default_path.exists():
            file_path = str(default_path)
            st.sidebar.success(f"✅ Using: {DEFAULT_DATA_PATH}")
        else:
            st.sidebar.warning("⚠️ Sample data not found")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV or Excel file",
            type=['csv', 'xlsx', 'xls']
        )
        if uploaded_file:
            # Save temporarily
            temp_path = Path(__file__).parent / "temp" / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_path = str(temp_path)
            st.sidebar.success(f"✅ Uploaded: {uploaded_file.name}")
    
    st.sidebar.markdown("---")
    
    # Filters (shown after data is loaded)
    st.sidebar.subheader("🔍 Filters")
    
    return file_path


# ============================================================================
# OVERVIEW SECTION
# ============================================================================

def render_overview(classified_df: pd.DataFrame, features_df: pd.DataFrame):
    """Render the overview section with key metrics and charts."""
    
    st.header("📊 Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Insights",
            value=f"{len(classified_df):,}",
            help="Total number of unique customer insights analyzed"
        )
    
    with col2:
        unique_companies = classified_df['cleaned_company'].nunique()
        st.metric(
            label="Companies Impacted",
            value=f"{unique_companies:,}",
            help="Number of unique companies providing feedback"
        )
    
    with col3:
        st.metric(
            label="Feature Clusters",
            value=len(features_df),
            help="Number of main feature clusters identified"
        )
    
    with col4:
        avg_rice = features_df['rice_score'].mean()
        st.metric(
            label="Avg. RICE Score",
            value=f"{avg_rice:.1f}",
            help="Average RICE score across all features"
        )
    
    st.markdown("---")
    
    # Year-wise breakdown (if date column exists)
    if 'created_at' in classified_df.columns or 'date' in classified_df.columns:
        date_col = 'created_at' if 'created_at' in classified_df.columns else 'date'
        st.subheader("📅 Year-wise Breakdown")
        
        # Convert to datetime if needed
        df_with_dates = classified_df.copy()
        df_with_dates[date_col] = pd.to_datetime(df_with_dates[date_col], errors='coerce')
        df_with_dates['year'] = df_with_dates[date_col].dt.year
        
        # Create year breakdown
        year_counts = df_with_dates['year'].value_counts().sort_index()
        year_companies = df_with_dates.groupby('year')['cleaned_company'].nunique()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=year_counts.index.astype(str),
                y=year_counts.values,
                labels={'x': 'Year', 'y': 'Insights'},
                title="Insights by Year",
                color_discrete_sequence=['#0070F2']
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                x=year_companies.index.astype(str),
                y=year_companies.values,
                labels={'x': 'Year', 'y': 'Companies'},
                title="Companies by Year",
                markers=True
            )
            fig.update_traces(line_color='#1A9898')
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution by Feature")
        
        # Prepare data for pie chart
        cluster_counts = classified_df['cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Feature', 'Count']
        
        fig = px.pie(
            cluster_counts,
            values='Count',
            names='Feature',
            color_discrete_sequence=CHART_COLORS,
            hole=0.4  # Makes it a donut chart
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Companies per Feature")
        
        # Horizontal bar chart of companies per feature
        company_counts = classified_df.groupby('cluster')['cleaned_company'].nunique().reset_index()
        company_counts.columns = ['Feature', 'Companies']
        company_counts = company_counts.sort_values('Companies', ascending=True)
        
        fig = px.bar(
            company_counts,
            x='Companies',
            y='Feature',
            orientation='h',
            color='Companies',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=400,
            yaxis_title="",
            xaxis_title="Number of Companies"
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # RICE score visualization
    st.subheader("Feature Priority (RICE Scores)")
    
    fig = px.bar(
        features_df.sort_values('rice_score', ascending=True),
        x='rice_score',
        y='feature_name',
        orientation='h',
        color='rice_score',
        color_continuous_scale='RdYlGn',
        text='rice_score'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        yaxis_title="",
        xaxis_title="RICE Score"
    )
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# FEATURE RANKING TABLE
# ============================================================================

def render_feature_ranking(features_df: pd.DataFrame, classified_df: pd.DataFrame):
    """Render the feature ranking table with RICE scores."""
    
    st.header("🏆 Feature Ranking")
    
    st.markdown("""
    Features are ranked by **RICE Score** (Reach × Impact × Confidence / Effort).
    Click on a feature row to see detailed information below.
    """)
    
    # Create a display version of the dataframe
    display_df = features_df.copy()
    display_df = display_df.rename(columns={
        'rank': 'Rank',
        'feature_name': 'Feature',
        'subfeatures': 'Sub-features',
        'insight_count': 'Insights',
        'company_count': 'Companies',
        'company_percentage': '% of Total',
        'impact': 'Impact',
        'confidence': 'Confidence',
        'effort': 'Effort',
        'rice_score': 'RICE Score'
    })
    
    # Select columns to display
    display_columns = [
        'Rank', 'Feature', 'Sub-features', 'Insights', 
        'Companies', '% of Total', 'RICE Score'
    ]
    
    # Style the dataframe
    def color_rice(val):
        """Color cells based on RICE score."""
        if val >= 10:
            return 'background-color: #90EE90'  # Light green
        elif val >= 5:
            return 'background-color: #FFFFE0'  # Light yellow
        else:
            return 'background-color: #FFB6C1'  # Light red
    
    styled_df = display_df[display_columns].style.applymap(
        color_rice, 
        subset=['RICE Score']
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    # Feature selector for detail view
    st.markdown("---")
    st.subheader("📋 Select a Feature for Details")
    
    selected_feature = st.selectbox(
        "Choose a feature to explore:",
        options=features_df['feature_name'].tolist(),
        format_func=lambda x: f"{x} (RICE: {features_df[features_df['feature_name']==x]['rice_score'].values[0]})"
    )
    
    return selected_feature


# ============================================================================
# FEATURE DETAIL VIEW
# ============================================================================

def render_feature_details(classified_df: pd.DataFrame, feature_name: str):
    """Render detailed information about a selected feature."""
    
    st.header(f"📋 {feature_name}")
    
    # Get feature details
    details = get_feature_details(classified_df, feature_name)
    
    if not details:
        st.error(f"No details found for feature: {feature_name}")
        return
    
    # RICE breakdown
    st.subheader("📊 RICE Score Breakdown")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Reach", details['reach'], help="Number of companies")
    with col2:
        st.metric("Impact", f"{details['impact']:.1f}", help="Severity (0.5-3.0)")
    with col3:
        st.metric("Confidence", f"{details['confidence']:.0%}", help="Data confidence")
    with col4:
        st.metric("Effort", details['effort'], help="Complexity (1-10)")
    with col5:
        st.metric("RICE Score", f"{details['rice_score']:.1f}", help="Final priority score")
    
    st.markdown("---")
    
    # Two-column layout for details
    col1, col2 = st.columns(2)
    
    with col1:
        # Problem Summary
        st.subheader("🎯 Problem Summary")
        st.markdown(details['problem_summary'])
        
        # Sub-features
        st.subheader("📦 Sub-features")
        
        if details['subfeatures']:
            for sf in details['subfeatures']:
                st.markdown(f"""
                <div class="feature-card">
                    <strong>{sf['subfeature']}</strong><br/>
                    <small>{sf['insights']} insights from {sf['companies']} companies</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Suggested Solutions
        st.subheader("💡 Suggested Solutions")
        for i, solution in enumerate(details['suggested_solutions'], 1):
            st.markdown(f"{i}. {solution}")
    
    with col2:
        # Sample Quotes
        st.subheader("💬 Sample Customer Quotes")
        
        if details['sample_quotes']:
            for quote in details['sample_quotes'][:MAX_SAMPLE_QUOTES]:
                st.markdown(f"""
                <div class="customer-quote">
                    "{quote['quote']}"
                    <br/><small>— {quote['company']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No sample quotes available")
        
        # Expected Benefits
        st.subheader("✅ Expected Benefits")
        for benefit in details['expected_benefits']:
            st.markdown(f"• {benefit}")
        
        # Business Outcomes
        st.subheader("📈 Business Outcomes")
        business_outcomes = [
            f"Reduce churn risk for {details['company_count']} requesting companies",
            "Increase product adoption and engagement metrics",
            "Strengthen competitive positioning in the market",
            f"Drive potential revenue growth of {details['company_count'] * 5}% ARR increase",
            "Improve customer satisfaction (NPS) scores"
        ]
        for outcome in business_outcomes:
            st.markdown(f"• {outcome}")
        
        # Companies List
        st.subheader("🏢 Companies Requesting This")
        companies_str = ", ".join(details['companies_list'][:10])
        if len(details['companies_list']) > 10:
            companies_str += f", and {len(details['companies_list']) - 10} more..."
        st.markdown(companies_str)
    
    st.markdown("---")
    
    # Roadmap Alignment Hint
    st.subheader("🗺️ Roadmap Considerations")
    st.info("""
    **To extend this for roadmap alignment:**
    1. Add a `roadmap_items` table with planned features
    2. Match feature names to roadmap items
    3. Show alignment status (Planned / In Progress / Not Planned)
    4. Calculate coverage percentage
    
    This helps identify gaps between customer needs and current plans.
    """)


# ============================================================================
# EXPORT FUNCTIONALITY
# ============================================================================

def render_export_section(features_df: pd.DataFrame, classified_df: pd.DataFrame):
    """Render export options."""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Export Data")
    
    # Export features summary
    if st.sidebar.button("Export Feature Summary"):
        csv = features_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="feature_summary.csv",
            mime="text/csv"
        )
    
    # Export classified insights
    if st.sidebar.button("Export All Insights"):
        csv = classified_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="classified_insights.csv",
            mime="text/csv"
        )


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Render sidebar and get file path
    file_path = render_sidebar()
    
    # Main title
    st.markdown('<h1 class="main-title">🎯 Customer Insight Intelligence Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("Analyze customer feedback, classify into strategic clusters, and prioritize with RICE scoring.")
    st.markdown("---")
    
    # Check if we have data
    if not file_path:
        st.warning("👆 Please select or upload a data file from the sidebar to get started.")
        
        # Show instructions
        st.markdown("""
        ### How to Use This Dashboard
        
        1. **Select Data Source**: Choose sample data or upload your own CSV/Excel file
        2. **Required Columns**: Your file should have:
           - `note_text` - The customer insight or feedback text
           - `company_name` - The organization providing the feedback
        3. **Explore Results**: Once loaded, you'll see:
           - Overview statistics and distribution charts
           - Feature ranking table with RICE scores
           - Detailed view for each feature
        
        ### What is RICE Scoring?
        
        RICE is a prioritization framework:
        - **R**each: How many customers want this?
        - **I**mpact: How important is it to them?
        - **C**onfidence: How sure are we about the data?
        - **E**ffort: How hard is it to build?
        
        Score = (Reach × Impact × Confidence) / Effort
        """)
        
        # Show cluster definitions
        with st.expander("📋 View Predefined Clusters"):
            for cluster, subclusters in CLUSTER_DEFINITIONS.items():
                st.markdown(f"**{cluster}**")
                for sub in subclusters:
                    st.markdown(f"  - {sub}")
        
        return
    
    # Load and process data
    with st.spinner("🔄 Loading and processing data... This may take a moment for large files."):
        try:
            classified_df, features_df, subfeatures_df = load_and_process_data(file_path)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.exception(e)
            return
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Feature Ranking", "📋 Feature Details"])
    
    with tab1:
        render_overview(classified_df, features_df)
    
    with tab2:
        selected_feature = render_feature_ranking(features_df, classified_df)
    
    with tab3:
        # Get feature from ranking tab or use first one
        if 'selected_feature' not in dir() or not selected_feature:
            selected_feature = features_df.iloc[0]['feature_name']
        
        feature_selector = st.selectbox(
            "Select Feature:",
            options=features_df['feature_name'].tolist(),
            key="detail_selector"
        )
        render_feature_details(classified_df, feature_selector)
    
    # Export functionality
    render_export_section(features_df, classified_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        Customer Insight Intelligence Dashboard | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    main()

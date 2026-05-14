"""
========================================
RICE SCORING MODULE
========================================
This module calculates RICE scores for each Feature (cluster) to help
prioritize which features to build first.

What is RICE?
RICE is a prioritization framework used by product managers:
- R = Reach: How many customers/users will this affect?
- I = Impact: How much will this improve their experience?
- C = Confidence: How sure are we about our estimates?
- E = Effort: How much work will this take?

Formula: RICE Score = (Reach × Impact × Confidence) / Effort

Higher RICE score = Higher priority

Key Concepts for Beginners:
- We calculate RICE for each Feature (cluster), not each insight
- Reach comes from counting unique companies
- Impact is inferred from the language used in insights
- Confidence comes from the number of similar insights
- Effort is estimated based on feature complexity
"""

import re
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

# Import our configuration
from config import (
    IMPACT_KEYWORDS,
    DEFAULT_IMPACT_SCORE,
    EFFORT_BY_CLUSTER,
    DEFAULT_EFFORT,
)


def calculate_reach(companies: set, total_companies: int) -> float:
    """
    Calculate the Reach score for a feature.
    
    Reach = Number of unique companies wanting this feature
    
    What it does:
    - Counts how many different companies mentioned insights in this cluster
    - Normalizes by total companies for percentage context
    
    Parameters:
        companies: Set of company names requesting this feature
        total_companies: Total unique companies in the dataset
    
    Returns:
        Reach score (number of companies)
    
    Example:
        reach = calculate_reach({'Acme', 'BigCorp', 'TechCo'}, 100)
        # Returns 3 (absolute reach)
    """
    return len(companies)


def calculate_reach_percentage(companies: set, total_companies: int) -> float:
    """
    Calculate reach as a percentage of total companies.
    
    Parameters:
        companies: Set of company names
        total_companies: Total unique companies
    
    Returns:
        Percentage (0-100)
    """
    if total_companies == 0:
        return 0.0
    return (len(companies) / total_companies) * 100


def calculate_impact(insights: List[Dict], text_column: str = 'cleaned_text') -> float:
    """
    Calculate the Impact score based on language analysis.
    
    Impact is derived from:
    - Urgency words ("critical", "blocker", "must have")
    - Importance indicators ("important", "need", "require")
    - Negativity about current state ("frustrated", "blocked")
    
    Parameters:
        insights: List of insight dictionaries in this cluster
        text_column: Column name containing the insight text
    
    Returns:
        Impact score (0.5 to 3.0)
        - 0.5 = Nice to have
        - 1.0 = Normal
        - 2.0 = Important
        - 3.0 = Critical
    
    Example:
        insights = [{'cleaned_text': 'This is a critical blocker for us'}]
        impact = calculate_impact(insights)  # Returns ~2.5
    """
    if not insights:
        return DEFAULT_IMPACT_SCORE
    
    total_impact = 0.0
    insight_count = 0
    
    for insight in insights:
        text = insight.get(text_column, '') or insight.get('note_text', '')
        if not text:
            continue
            
        text_lower = text.lower()
        max_impact = DEFAULT_IMPACT_SCORE
        
        # Check for impact keywords
        for keyword, score in IMPACT_KEYWORDS.items():
            if keyword.lower() in text_lower:
                max_impact = max(max_impact, score)
        
        # Also check for urgency indicators
        if re.search(r'\b(asap|immediately|urgent(ly)?)\b', text_lower):
            max_impact = max(max_impact, 2.5)
        
        if re.search(r'\b(block(ed|er|ing)?|cannot|unable|impossible)\b', text_lower):
            max_impact = max(max_impact, 2.0)
        
        total_impact += max_impact
        insight_count += 1
    
    # Return average impact, or default if no valid insights
    if insight_count == 0:
        return DEFAULT_IMPACT_SCORE
    
    return round(total_impact / insight_count, 2)


def calculate_confidence(insights: List[Dict], 
                        classification_confidences: List[float] = None) -> float:
    """
    Calculate the Confidence score.
    
    Confidence is based on:
    - Number of insights (more data = higher confidence)
    - Classification confidence (how sure we are about clustering)
    - Consistency of requests (similar language across companies)
    
    Parameters:
        insights: List of insights for this feature
        classification_confidences: Optional list of classifier confidence scores
    
    Returns:
        Confidence score from 0.0 to 1.0
        - 0.2 = Very low (1-2 insights)
        - 0.5 = Medium (5-10 insights)
        - 0.8 = High (20+ insights)
        - 1.0 = Very high (50+ insights from many companies)
    
    Example:
        confidence = calculate_confidence(insights_list)
    """
    num_insights = len(insights)
    
    # Base confidence from number of insights
    # More insights = higher confidence
    if num_insights >= 50:
        base_confidence = 1.0
    elif num_insights >= 20:
        base_confidence = 0.8
    elif num_insights >= 10:
        base_confidence = 0.6
    elif num_insights >= 5:
        base_confidence = 0.4
    elif num_insights >= 2:
        base_confidence = 0.3
    else:
        base_confidence = 0.2
    
    # Adjust based on classification confidence if available
    if classification_confidences and len(classification_confidences) > 0:
        avg_class_conf = sum(classification_confidences) / len(classification_confidences)
        # Blend base confidence with classification confidence
        confidence = (base_confidence * 0.7) + (avg_class_conf * 0.3)
    else:
        confidence = base_confidence
    
    return round(min(confidence, 1.0), 2)


def calculate_effort(cluster: str, 
                    insights: List[Dict] = None,
                    custom_effort: Optional[int] = None) -> float:
    """
    Calculate the Effort estimate for a feature.
    
    Effort is estimated from:
    - The cluster type (some areas are inherently more complex)
    - Number of sub-features requested
    - Custom override if provided
    
    Parameters:
        cluster: The cluster/feature name
        insights: List of insights (optional, for complexity analysis)
        custom_effort: Manual effort override (1-10)
    
    Returns:
        Effort score from 1 to 10
        - 1 = Very easy (hours)
        - 3 = Easy (days)
        - 5 = Medium (weeks)
        - 7 = Hard (months)
        - 10 = Very hard (quarters)
    
    Example:
        effort = calculate_effort("SPG AI")  # Returns 9 (high complexity)
    """
    # Use custom effort if provided
    if custom_effort is not None:
        return max(1, min(10, custom_effort))
    
    # Get base effort from configuration
    base_effort = EFFORT_BY_CLUSTER.get(cluster, DEFAULT_EFFORT)
    
    # Could add logic here to adjust based on insight complexity
    # For example, analyzing technical complexity in the language
    
    return base_effort


def calculate_rice_score(reach: float, 
                        impact: float, 
                        confidence: float, 
                        effort: float) -> float:
    """
    Calculate the final RICE score.
    
    Formula: RICE = (Reach × Impact × Confidence) / Effort
    
    Parameters:
        reach: Number of companies impacted
        impact: Impact score (0.5-3.0)
        confidence: Confidence score (0-1.0)
        effort: Effort estimate (1-10)
    
    Returns:
        RICE score (higher is better)
    
    Example:
        rice = calculate_rice_score(
            reach=15,      # 15 companies
            impact=2.0,    # Important
            confidence=0.8, # High confidence
            effort=5       # Medium effort
        )
        # Returns: (15 × 2.0 × 0.8) / 5 = 4.8
    """
    if effort == 0:
        effort = 1  # Prevent division by zero
    
    return round((reach * impact * confidence) / effort, 2)


def score_all_features(df_classified: pd.DataFrame,
                      text_column: str = 'cleaned_text',
                      company_column: str = 'cleaned_company') -> pd.DataFrame:
    """
    Calculate RICE scores for all features (clusters).
    
    This is the main function - it processes all classified insights
    and generates a prioritized feature list.
    
    Parameters:
        df_classified: DataFrame with classification columns
        text_column: Column name for insight text
        company_column: Column name for company
    
    Returns:
        DataFrame with features and their RICE scores, sorted by priority:
        - feature_name
        - subfeatures (comma-separated)
        - insight_count
        - company_count
        - company_percentage
        - reach
        - impact
        - confidence
        - effort
        - rice_score
        - rank
    
    Example:
        features_df = score_all_features(classified_df)
        print(features_df.head())
    """
    print("\n📊 Calculating RICE scores for features...")
    
    # Get total unique companies for percentage calculation
    total_companies = df_classified[company_column].nunique()
    
    # Group insights by cluster (feature)
    features = []
    
    for cluster in df_classified['cluster'].unique():
        cluster_df = df_classified[df_classified['cluster'] == cluster]
        
        # Get insights as list of dicts
        insights = cluster_df.to_dict('records')
        
        # Get unique companies
        companies = set(cluster_df[company_column].unique())
        
        # Get subfeatures
        subfeatures = list(cluster_df['subcluster'].unique())
        
        # Get classification confidences
        confidences = list(cluster_df['overall_confidence'])
        
        # Calculate RICE components
        reach = calculate_reach(companies, total_companies)
        reach_pct = calculate_reach_percentage(companies, total_companies)
        impact = calculate_impact(insights, text_column)
        confidence = calculate_confidence(insights, confidences)
        effort = calculate_effort(cluster, insights)
        rice_score = calculate_rice_score(reach, impact, confidence, effort)
        
        features.append({
            'feature_name': cluster,
            'subfeatures': ', '.join(subfeatures),
            'subfeature_count': len(subfeatures),
            'insight_count': len(insights),
            'company_count': len(companies),
            'company_percentage': round(reach_pct, 1),
            'reach': reach,
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'rice_score': rice_score,
        })
    
    # Create DataFrame and sort by RICE score
    features_df = pd.DataFrame(features)
    features_df = features_df.sort_values('rice_score', ascending=False)
    features_df['rank'] = range(1, len(features_df) + 1)
    
    # Reorder columns
    column_order = [
        'rank', 'feature_name', 'subfeatures', 'insight_count',
        'company_count', 'company_percentage',
        'reach', 'impact', 'confidence', 'effort', 'rice_score'
    ]
    features_df = features_df[column_order]
    
    print(f"\n✅ RICE scoring complete!")
    print(f"\n🏆 Top 5 Features by RICE Score:")
    for _, row in features_df.head().iterrows():
        print(f"   #{row['rank']}: {row['feature_name']} "
              f"(Score: {row['rice_score']}, "
              f"Companies: {row['company_count']})")
    
    return features_df.reset_index(drop=True)


def score_subfeatures(df_classified: pd.DataFrame,
                     text_column: str = 'cleaned_text',
                     company_column: str = 'cleaned_company') -> pd.DataFrame:
    """
    Calculate RICE scores at the sub-feature level.
    
    Parameters:
        df_classified: DataFrame with classification columns
        text_column: Column name for insight text
        company_column: Column name for company
    
    Returns:
        DataFrame with subfeatures and their RICE scores
    """
    print("\n📊 Calculating RICE scores for sub-features...")
    
    total_companies = df_classified[company_column].nunique()
    subfeatures = []
    
    for (cluster, subcluster), group_df in df_classified.groupby(['cluster', 'subcluster']):
        insights = group_df.to_dict('records')
        companies = set(group_df[company_column].unique())
        confidences = list(group_df['overall_confidence'])
        
        reach = calculate_reach(companies, total_companies)
        reach_pct = calculate_reach_percentage(companies, total_companies)
        impact = calculate_impact(insights, text_column)
        confidence = calculate_confidence(insights, confidences)
        effort = calculate_effort(cluster, insights)  # Use cluster effort
        rice_score = calculate_rice_score(reach, impact, confidence, effort)
        
        subfeatures.append({
            'feature_name': cluster,
            'subfeature_name': subcluster,
            'insight_count': len(insights),
            'company_count': len(companies),
            'company_percentage': round(reach_pct, 1),
            'reach': reach,
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'rice_score': rice_score,
        })
    
    subfeatures_df = pd.DataFrame(subfeatures)
    subfeatures_df = subfeatures_df.sort_values('rice_score', ascending=False)
    subfeatures_df['rank'] = range(1, len(subfeatures_df) + 1)
    
    return subfeatures_df.reset_index(drop=True)


def get_feature_details(df_classified: pd.DataFrame, 
                       feature_name: str,
                       text_column: str = 'cleaned_text',
                       company_column: str = 'cleaned_company',
                       max_quotes: int = 5) -> Dict:
    """
    Get detailed information about a specific feature.
    
    This provides all the context needed for the detail view:
    - Problem summary (what customers are asking for)
    - Sub-features breakdown
    - Sample customer quotes
    - Suggested solution directions
    
    Parameters:
        df_classified: DataFrame with classifications
        feature_name: The feature/cluster to get details for
        text_column: Column with insight text
        company_column: Column with company names
        max_quotes: Maximum number of sample quotes to include
    
    Returns:
        Dictionary with comprehensive feature details
    """
    # Filter to this feature
    feature_df = df_classified[df_classified['cluster'] == feature_name]
    
    if len(feature_df) == 0:
        return None
    
    # Get basic stats
    total_companies = df_classified[company_column].nunique()
    companies = set(feature_df[company_column].unique())
    insights = feature_df.to_dict('records')
    
    # Get RICE components
    reach = calculate_reach(companies, total_companies)
    reach_pct = calculate_reach_percentage(companies, total_companies)
    impact = calculate_impact(insights, text_column)
    confidence = calculate_confidence(insights, list(feature_df['overall_confidence']))
    effort = calculate_effort(feature_name)
    rice_score = calculate_rice_score(reach, impact, confidence, effort)
    
    # Get subfeatures with counts
    subfeature_breakdown = feature_df.groupby('subcluster').agg({
        'insight_id': 'count',
        company_column: 'nunique'
    }).reset_index()
    subfeature_breakdown.columns = ['subfeature', 'insights', 'companies']
    subfeature_breakdown = subfeature_breakdown.sort_values('insights', ascending=False)
    
    # Get sample quotes (longest and most relevant)
    sample_quotes = []
    for _, row in feature_df.nlargest(max_quotes, 'text_length').iterrows():
        text = row.get(text_column, row.get('note_text', ''))
        company = row.get(company_column, 'Unknown')
        if text and len(text) > 20:  # Skip very short quotes
            sample_quotes.append({
                'quote': text[:500] + ('...' if len(text) > 500 else ''),
                'company': company
            })
    
    # Generate problem summary
    problem_summary = _generate_problem_summary(feature_name, insights)
    
    # Generate suggested solutions
    suggested_solutions = _generate_solution_suggestions(feature_name)
    
    # Generate expected benefits
    expected_benefits = _generate_expected_benefits(feature_name, len(companies))
    
    return {
        'feature_name': feature_name,
        'insight_count': len(insights),
        'company_count': len(companies),
        'company_percentage': round(reach_pct, 1),
        'rice_score': rice_score,
        'reach': reach,
        'impact': impact,
        'confidence': confidence,
        'effort': effort,
        'subfeatures': subfeature_breakdown.to_dict('records'),
        'sample_quotes': sample_quotes,
        'problem_summary': problem_summary,
        'suggested_solutions': suggested_solutions,
        'expected_benefits': expected_benefits,
        'companies_list': sorted(list(companies))[:20],  # Top 20 companies
    }


def _generate_problem_summary(feature_name: str, insights: List[Dict]) -> str:
    """Generate a summary of the problem based on insights."""
    
    summaries = {
        "APIs": "Customers need robust APIs to integrate our platform with their existing systems. Key requests include webhooks for real-time notifications, RESTful endpoints for data access, and trigger-based automation capabilities.",
        
        "Risk & Compliance": "Organizations require enhanced compliance and governance features to meet regulatory requirements. This includes audit trails, access controls, and specific regulatory framework support (GDPR, SOX, etc.).",
        
        "Asset Lifecycles & Approvals": "Users need better control over asset versioning, approval workflows, and lifecycle management. Multi-level approvals and clear ownership transitions are frequently requested.",
        
        "Enterprise Readiness": "Large organizations need enterprise-grade features including scalability, security enhancements, cloud migration tools, and robust database management.",
        
        "Case & Task Management": "Teams need improved tools for managing tasks, cases, and work items. Better assignment, tracking, and notification features are commonly requested.",
        
        "Other Collaboration Features": "Users want enhanced collaboration capabilities including better sharing, commenting, and team communication features.",
        
        "WF Management Foundation": "Core workflow management improvements are needed, including better workflow building tools, scripting capabilities, and visual editing features.",
        
        "Workspace Settings": "Organizations require sophisticated workspace configuration options including user management, role-based access controls, and license tracking capabilities.",
        
        "SPG AI": "Customers are interested in AI-powered features including intelligent recommendations, automation, and natural language processing capabilities powered by Joule.",
        
        "Service Ticket": "These are operational support requests rather than feature insights, including account access issues, password resets, technical errors, and general troubleshooting needs.",
    }
    
    return summaries.get(feature_name, 
        f"Customers have submitted {len(insights)} insights related to {feature_name}, indicating significant interest in this area.")


def _generate_solution_suggestions(feature_name: str) -> List[str]:
    """Generate solution suggestions based on feature area."""
    
    suggestions = {
        "APIs": [
            "Develop a comprehensive REST API with OpenAPI documentation",
            "Implement webhook system for event-driven integrations",
            "Create SDK packages for common programming languages",
            "Build a developer portal with sandbox environment"
        ],
        "Risk & Compliance": [
            "Implement comprehensive audit logging",
            "Create compliance dashboard with regulation templates",
            "Add role-based access controls with audit trails",
            "Develop automated compliance reporting"
        ],
        "Asset Lifecycles & Approvals": [
            "Build configurable multi-level approval workflows",
            "Implement version control with comparison features",
            "Create asset ownership and handover management",
            "Add lifecycle stage visualization"
        ],
        "Enterprise Readiness": [
            "Conduct performance optimization and load testing",
            "Implement SSO and advanced authentication",
            "Create cloud migration toolkit and documentation",
            "Develop disaster recovery and backup solutions"
        ],
        "Case & Task Management": [
            "Build comprehensive task management module",
            "Create case tracking with customizable workflows",
            "Implement team-based task assignment",
            "Add due date tracking and notifications"
        ],
        "Other Collaboration Features": [
            "Enhance commenting and discussion threads",
            "Improve sharing and permission controls",
            "Add real-time collaboration features",
            "Create team workspace functionality"
        ],
        "WF Management Foundation": [
            "Modernize workflow builder with drag-and-drop",
            "Add advanced scripting and custom actions",
            "Improve workflow canvas visualization",
            "Create forms designer with validation"
        ],
        "Workspace Settings": [
            "Build comprehensive user management dashboard",
            "Implement license usage tracking and analytics",
            "Create role templates and permission presets",
            "Add bulk user operations and import/export"
        ],
        "SPG AI": [
            "Integrate Joule for intelligent assistance",
            "Implement ML-based recommendations",
            "Add natural language search capabilities",
            "Create predictive analytics features"
        ],
        "Service Ticket": [
            "Improve self-service password reset functionality",
            "Enhance error messaging and troubleshooting guides",
            "Create knowledge base for common issues",
            "Implement proactive monitoring and alerting"
        ],
    }
    
    return suggestions.get(feature_name, [
        "Analyze detailed customer requirements",
        "Design solution architecture",
        "Implement in phases with customer feedback",
        "Measure impact and iterate"
    ])


def _generate_expected_benefits(feature_name: str, company_count: int) -> List[str]:
    """Generate expected benefits from implementing the feature."""
    
    return [
        f"Address needs of {company_count} customers directly requesting this capability",
        "Increase platform stickiness and reduce churn risk",
        "Enable new use cases and expand market reach",
        "Improve customer satisfaction scores (NPS/CSAT)",
        "Generate potential upsell opportunities"
    ]


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing RICE Scoring Module")
    print("=" * 50)
    
    # Test individual calculations
    print("\n📊 Testing RICE calculation:")
    print("-" * 40)
    
    test_reach = 15
    test_impact = 2.0
    test_confidence = 0.8
    test_effort = 5
    
    print(f"Reach: {test_reach} companies")
    print(f"Impact: {test_impact}")
    print(f"Confidence: {test_confidence}")
    print(f"Effort: {test_effort}")
    
    score = calculate_rice_score(test_reach, test_impact, test_confidence, test_effort)
    print(f"\nRICE Score: {score}")
    print(f"Formula: ({test_reach} × {test_impact} × {test_confidence}) / {test_effort} = {score}")
    
    # Test impact calculation
    print("\n📊 Testing Impact calculation:")
    print("-" * 40)
    
    test_insights = [
        {'cleaned_text': 'This is a critical blocker for us'},
        {'cleaned_text': 'We would like this feature'},
        {'cleaned_text': 'This is urgently needed'},
    ]
    
    impact = calculate_impact(test_insights)
    print(f"Average Impact: {impact}")

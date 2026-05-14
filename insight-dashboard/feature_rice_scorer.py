"""
========================================
FEATURE RICE SCORING MODULE
========================================
This module calculates RICE scores for Features (not clusters).

RICE Score = (Reach × Impact × Confidence) / Effort

For Features:
- Reach = Number of unique companies requesting this feature
- Impact = Severity derived from language in insights
- Confidence = Based on number of supporting insights
- Effort = Estimated based on feature type/complexity
"""

import re
from typing import Dict, List
import pandas as pd

from config import IMPACT_KEYWORDS, DEFAULT_IMPACT_SCORE, EFFORT_BY_CLUSTER, DEFAULT_EFFORT


# Feature complexity estimates (effort modifier)
FEATURE_EFFORT_MODIFIERS = {
    # High effort features (modifier: 1.5x)
    "SSO Integration": 1.5,
    "Cloud Migration": 1.5,
    "API Integration": 1.3,
    "Predictive Analytics": 1.5,
    "Joule Integration": 1.5,
    
    # Medium effort features (modifier: 1.0x - default)
    "Workflow Builder": 1.2,
    "Approval Workflow": 1.1,
    "User Management": 1.0,
    "Role Management": 1.0,
    
    # Lower effort features (modifier: 0.7-0.9x)
    "Notification System": 0.8,
    "Comments & Discussions": 0.7,
    "Sharing & Permissions": 0.8,
    "Due Date Tracking": 0.7,
}


def calculate_feature_reach(companies: List[str], total_companies: int) -> int:
    """Calculate reach as number of unique companies."""
    return len(set(companies))


def calculate_feature_reach_pct(companies: List[str], total_companies: int) -> float:
    """Calculate reach as percentage of total companies."""
    if total_companies == 0:
        return 0.0
    return round((len(set(companies)) / total_companies) * 100, 1)


def calculate_feature_impact(sample_quotes: List[str]) -> float:
    """
    Calculate impact score based on language in feature's insights.
    
    Returns score from 0.5 to 3.0
    """
    if not sample_quotes:
        return DEFAULT_IMPACT_SCORE
    
    total_impact = 0.0
    quote_count = 0
    
    for quote in sample_quotes:
        if not quote:
            continue
        
        quote_lower = str(quote).lower()
        max_impact = DEFAULT_IMPACT_SCORE
        
        # Check for impact keywords
        for keyword, score in IMPACT_KEYWORDS.items():
            if keyword.lower() in quote_lower:
                max_impact = max(max_impact, score)
        
        # Check for urgency indicators
        if re.search(r'\b(asap|immediately|urgent(ly)?)\b', quote_lower):
            max_impact = max(max_impact, 2.5)
        
        if re.search(r'\b(block(ed|er|ing)?|cannot|unable|impossible)\b', quote_lower):
            max_impact = max(max_impact, 2.0)
        
        if re.search(r'\b(critical|crucial|essential)\b', quote_lower):
            max_impact = max(max_impact, 2.5)
        
        total_impact += max_impact
        quote_count += 1
    
    if quote_count == 0:
        return DEFAULT_IMPACT_SCORE
    
    return round(total_impact / quote_count, 2)


def calculate_feature_confidence(insight_count: int, company_count: int) -> float:
    """
    Calculate confidence based on data volume.
    
    More insights and more companies = higher confidence.
    """
    # Base confidence from insight count
    if insight_count >= 20:
        base_conf = 0.95
    elif insight_count >= 10:
        base_conf = 0.8
    elif insight_count >= 5:
        base_conf = 0.6
    elif insight_count >= 3:
        base_conf = 0.5
    elif insight_count >= 2:
        base_conf = 0.4
    else:
        base_conf = 0.3
    
    # Boost for multiple companies
    company_boost = min(company_count / 10, 0.2)  # Up to 0.2 boost
    
    return round(min(base_conf + company_boost, 1.0), 2)


def calculate_feature_effort(feature_name: str, cluster: str) -> int:
    """
    Calculate effort estimate for a feature.
    
    Uses cluster base effort with feature-specific modifiers.
    """
    # Get base effort from cluster
    base_effort = EFFORT_BY_CLUSTER.get(cluster, DEFAULT_EFFORT)
    
    # Apply feature modifier if exists
    modifier = FEATURE_EFFORT_MODIFIERS.get(feature_name, 1.0)
    
    effort = int(round(base_effort * modifier))
    
    # Clamp between 1 and 10
    return max(1, min(10, effort))


def calculate_feature_rice(reach: int, impact: float, 
                           confidence: float, effort: int) -> float:
    """
    Calculate RICE score.
    
    RICE = (Reach × Impact × Confidence) / Effort
    """
    if effort == 0:
        effort = 1
    
    return round((reach * impact * confidence) / effort, 2)


def score_features(features_df: pd.DataFrame, 
                   total_companies: int) -> pd.DataFrame:
    """
    Calculate RICE scores for all features.
    
    Parameters:
        features_df: DataFrame from feature_extractor
        total_companies: Total unique companies in dataset
    
    Returns:
        DataFrame with RICE components and scores
    """
    print("\n📊 Calculating RICE scores for features...")
    
    scored_features = []
    
    for _, feature in features_df.iterrows():
        reach = calculate_feature_reach(feature['companies'], total_companies)
        reach_pct = calculate_feature_reach_pct(feature['companies'], total_companies)
        impact = calculate_feature_impact(feature.get('sample_quotes', []))
        confidence = calculate_feature_confidence(
            feature['insight_count'], 
            feature['company_count']
        )
        effort = calculate_feature_effort(feature['feature_name'], feature['cluster'])
        rice_score = calculate_feature_rice(reach, impact, confidence, effort)
        
        scored_features.append({
            'feature_id': feature['feature_id'],
            'feature_name': feature['feature_name'],
            'cluster': feature['cluster'],
            'insight_count': feature['insight_count'],
            'company_count': feature['company_count'],
            'reach': reach,
            'reach_pct': reach_pct,
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'rice_score': rice_score,
            'companies': feature['companies'],
            'sample_quotes': feature.get('sample_quotes', []),
            'year_distribution': feature.get('year_distribution', {}),
        })
    
    scored_df = pd.DataFrame(scored_features)
    scored_df = scored_df.sort_values('rice_score', ascending=False)
    scored_df['rank'] = range(1, len(scored_df) + 1)
    
    print(f"\n🏆 Top 10 Features by RICE Score:")
    for _, row in scored_df.head(10).iterrows():
        print(f"   #{row['rank']}: {row['feature_name'][:40]} "
              f"(RICE: {row['rice_score']}, Reach: {row['reach']} companies)")
    
    return scored_df.reset_index(drop=True)


def get_feature_details(scored_features_df: pd.DataFrame, 
                        feature_id: int) -> Dict:
    """
    Get detailed information about a specific feature.
    """
    feature = scored_features_df[scored_features_df['feature_id'] == feature_id]
    
    if len(feature) == 0:
        return None
    
    feature = feature.iloc[0]
    
    return {
        'feature_id': feature['feature_id'],
        'feature_name': feature['feature_name'],
        'cluster': feature['cluster'],
        'insight_count': feature['insight_count'],
        'company_count': feature['company_count'],
        'reach': feature['reach'],
        'reach_pct': feature['reach_pct'],
        'impact': feature['impact'],
        'confidence': feature['confidence'],
        'effort': feature['effort'],
        'rice_score': feature['rice_score'],
        'sample_quotes': feature['sample_quotes'],
        'companies': feature['companies'][:20],
        'year_distribution': feature['year_distribution'],
    }


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Feature RICE Scoring")
    print("=" * 50)
    
    # Test individual calculations
    print("\n📊 Sample RICE Calculation:")
    
    reach = 15
    impact = 2.0
    confidence = 0.7
    effort = 5
    
    rice = calculate_feature_rice(reach, impact, confidence, effort)
    
    print(f"  Reach: {reach} companies")
    print(f"  Impact: {impact}")
    print(f"  Confidence: {confidence}")
    print(f"  Effort: {effort}")
    print(f"  RICE Score: {rice}")
    print(f"  Formula: ({reach} × {impact} × {confidence}) / {effort} = {rice}")

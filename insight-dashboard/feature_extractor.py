"""
========================================
FEATURE EXTRACTOR MODULE
========================================
This module analyzes customer insights and derives potential product features.
It groups similar insights into features and sub-features.

What this module does:
1. Analyzes insight text to derive a feature title
2. Groups similar insights into the same feature
3. Creates sub-features where applicable
4. Maps multiple insights to features with counts

Key Concepts:
- "Feature" = A potential product capability derived from insights
- "Sub-feature" = A more specific aspect of a feature
- Multiple insights can map to one feature
"""

import re
from typing import Dict, List, Tuple, Optional
import pandas as pd
from collections import defaultdict
import hashlib

from config import CLUSTER_DEFINITIONS, CLASSIFICATION_KEYWORDS


# Feature patterns to detect common request types
FEATURE_PATTERNS = {
    # API Features
    "API Export": [r"export.*(api|data|report)", r"api.*(export|extract)", r"download.*api"],
    "API Integration": [r"integrat.*(api|system|third)", r"connect.*(api|external)", r"api.*connect"],
    "Webhook Triggers": [r"webhook", r"trigger.*event", r"event.*trigger", r"callback"],
    "REST API Access": [r"rest.*api", r"api.*access", r"api.*endpoint"],
    
    # Risk & Compliance Features
    "Audit Trail": [r"audit.*trail", r"track.*change", r"history.*change", r"log.*action"],
    "Compliance Reporting": [r"compliance.*report", r"regulat.*report", r"audit.*report"],
    "Access Control Audit": [r"access.*audit", r"permission.*track", r"who.*access"],
    "Risk Assessment": [r"risk.*assess", r"risk.*evaluat", r"risk.*score"],
    
    # Asset Lifecycle Features
    "Version Control": [r"version.*control", r"version.*manag", r"track.*version", r"revision"],
    "Approval Workflow": [r"approval.*workflow", r"multi.*level.*approv", r"sign.*off", r"review.*approv"],
    "Asset Publishing": [r"publish.*asset", r"release.*process", r"deploy.*process"],
    "Asset Archiving": [r"archive", r"deprecat", r"retire.*process"],
    
    # Enterprise Readiness Features
    "SSO Integration": [r"sso", r"single.*sign.*on", r"saml", r"ldap.*auth"],
    "Cloud Migration": [r"cloud.*migrat", r"move.*cloud", r"saas.*migrat"],
    "Performance Optimization": [r"perform.*optim", r"speed", r"faster", r"slow.*load"],
    "Data Backup": [r"backup", r"disaster.*recover", r"data.*restore"],
    
    # Case & Task Management Features
    "Task Assignment": [r"task.*assign", r"assign.*task", r"delegate.*task", r"responsib"],
    "Due Date Tracking": [r"due.*date", r"deadline", r"timeline.*track"],
    "Case Status Tracking": [r"case.*status", r"status.*track", r"progress.*track"],
    "Notification System": [r"notif", r"alert", r"remind", r"email.*notif"],
    
    # Collaboration Features
    "Comments & Discussions": [r"comment", r"discuss", r"feedback.*thread", r"annotat"],
    "Sharing & Permissions": [r"shar.*permission", r"share.*access", r"collaborat.*share"],
    "Real-time Collaboration": [r"real.*time.*collab", r"co.*edit", r"simultaneous.*edit"],
    "Mentions & Tagging": [r"mention", r"tag.*user", r"@.*notif"],
    
    # WF Management Features
    "Workflow Builder": [r"workflow.*build", r"create.*workflow", r"design.*workflow", r"workflow.*design"],
    "Form Designer": [r"form.*design", r"form.*build", r"form.*edit", r"form.*creat"],
    "Script Actions": [r"script.*action", r"custom.*script", r"automat.*script"],
    "Workflow Canvas": [r"canvas", r"visual.*workflow", r"drag.*drop", r"bpmn.*edit"],
    "Conditional Logic": [r"condition.*logic", r"if.*then", r"branch.*logic", r"gateway"],
    
    # Workspace Settings Features
    "User Management": [r"user.*manag", r"add.*user", r"remove.*user", r"user.*admin"],
    "Role Management": [r"role.*manag", r"permission.*role", r"access.*role"],
    "License Management": [r"license.*manag", r"seat.*manag", r"subscription"],
    "Workspace Configuration": [r"workspace.*config", r"setting.*config", r"preference"],
    
    # SPG AI Features
    "AI Recommendations": [r"ai.*recommend", r"intelligent.*suggest", r"smart.*suggest"],
    "Natural Language Search": [r"natural.*language", r"nlp.*search", r"ai.*search"],
    "Joule Integration": [r"joule", r"ai.*assist", r"copilot"],
    "Predictive Analytics": [r"predict.*analytic", r"forecast", r"ai.*analyz"],
}

# Generic feature templates by cluster
CLUSTER_FEATURE_TEMPLATES = {
    "APIs": "API {action} for {subject}",
    "Risk & Compliance": "{subject} {action} capabilities",
    "Asset Lifecycles & Approvals": "{subject} {action} management",
    "Enterprise Readiness": "Enterprise {subject} {action}",
    "Case & Task Management": "{subject} {action} functionality",
    "Other Collaboration Features": "Collaboration {action} for {subject}",
    "WF Management Foundation": "Workflow {subject} {action}",
    "Workspace Settings": "{subject} {action} settings",
    "SPG AI": "AI-powered {subject} {action}",
    "Service Ticket": "Support: {subject}",
}


def extract_key_phrases(text: str) -> List[str]:
    """Extract key phrases/nouns from text that might indicate features."""
    if not text:
        return []
    
    # Common action words
    actions = [
        'export', 'import', 'create', 'delete', 'update', 'manage', 'track',
        'view', 'edit', 'share', 'publish', 'approve', 'reject', 'assign',
        'notify', 'alert', 'search', 'filter', 'sort', 'integrate', 'connect',
        'automate', 'configure', 'customize', 'report', 'analyze', 'monitor'
    ]
    
    # Common subjects
    subjects = [
        'workflow', 'process', 'task', 'case', 'user', 'role', 'permission',
        'data', 'report', 'form', 'field', 'document', 'asset', 'version',
        'comment', 'notification', 'email', 'status', 'dashboard', 'api',
        'integration', 'audit', 'log', 'backup', 'template', 'diagram'
    ]
    
    text_lower = text.lower()
    found_actions = [a for a in actions if a in text_lower]
    found_subjects = [s for s in subjects if s in text_lower]
    
    return found_actions + found_subjects


def derive_feature_title(text: str, cluster: str) -> str:
    """
    Derive a feature title from insight text.
    
    Uses pattern matching and key phrase extraction to generate
    a meaningful feature name.
    """
    if not text:
        return f"{cluster} Enhancement"
    
    text_lower = text.lower()
    
    # First, try to match against known feature patterns
    for feature_name, patterns in FEATURE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return feature_name
    
    # Extract key phrases
    phrases = extract_key_phrases(text)
    
    if phrases:
        # Try to construct a feature name from phrases
        actions = ['export', 'import', 'create', 'manage', 'track', 'view', 
                   'edit', 'share', 'publish', 'approve', 'integrate', 'automate']
        subjects = ['workflow', 'process', 'task', 'case', 'user', 'data', 
                   'report', 'form', 'document', 'notification', 'api']
        
        found_action = next((p for p in phrases if p in actions), None)
        found_subject = next((p for p in phrases if p in subjects), None)
        
        if found_action and found_subject:
            return f"{found_subject.title()} {found_action.title()}"
        elif found_subject:
            return f"{found_subject.title()} Enhancement"
        elif found_action:
            return f"{found_action.title()} Capability"
    
    # Fallback: use first significant words from text
    words = text.split()[:10]
    significant_words = [w for w in words if len(w) > 4 and w.isalpha()]
    if significant_words:
        return f"{significant_words[0].title()} Feature"
    
    return f"{cluster} Enhancement"


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity between two texts using word overlap.
    Returns a score between 0 and 1.
    """
    if not text1 or not text2:
        return 0.0
    
    words1 = set(re.findall(r'\b\w{4,}\b', text1.lower()))
    words2 = set(re.findall(r'\b\w{4,}\b', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def group_insights_into_features(df: pd.DataFrame, 
                                  text_column: str = 'cleaned_text',
                                  cluster_column: str = 'cluster',
                                  company_column: str = 'cleaned_company',
                                  similarity_threshold: float = 0.3) -> pd.DataFrame:
    """
    Group similar insights into features.
    
    Process:
    1. For each cluster, analyze all insights
    2. Derive feature titles from insights
    3. Group similar insights under the same feature
    4. Track insight count and companies per feature
    
    Returns DataFrame with features and their mapped insights.
    """
    print("\n🔬 Extracting features from insights...")
    
    features_data = []
    feature_id = 0
    
    # Process each cluster
    for cluster in df[cluster_column].unique():
        cluster_df = df[df[cluster_column] == cluster].copy()
        
        # Dictionary to hold features for this cluster
        cluster_features = {}
        
        for idx, row in cluster_df.iterrows():
            text = row.get(text_column, '') or row.get('note_text', '')
            company = row.get(company_column, 'Unknown')
            
            if not text or len(str(text)) < 10:
                continue
            
            # Derive feature title
            feature_title = derive_feature_title(str(text), cluster)
            
            # Check if this feature already exists or is similar to existing
            matched_feature = None
            best_similarity = 0
            
            for existing_title, feature_data in cluster_features.items():
                # Check title similarity
                title_sim = compute_similarity(feature_title, existing_title)
                
                # Also check text similarity with existing insights
                for existing_text in feature_data['sample_texts'][:3]:
                    text_sim = compute_similarity(str(text), existing_text)
                    if text_sim > best_similarity:
                        best_similarity = text_sim
                        if text_sim > similarity_threshold:
                            matched_feature = existing_title
            
            # Title exact match takes precedence
            if feature_title in cluster_features:
                matched_feature = feature_title
            
            if matched_feature:
                # Add to existing feature
                cluster_features[matched_feature]['insights'].append(row.to_dict())
                cluster_features[matched_feature]['companies'].add(company)
                if len(cluster_features[matched_feature]['sample_texts']) < 10:
                    cluster_features[matched_feature]['sample_texts'].append(str(text))
            else:
                # Create new feature
                cluster_features[feature_title] = {
                    'insights': [row.to_dict()],
                    'companies': {company},
                    'sample_texts': [str(text)],
                    'cluster': cluster,
                }
        
        # Convert cluster features to records
        for feature_title, feature_data in cluster_features.items():
            feature_id += 1
            
            # Get year distribution if date column exists
            year_distribution = {}
            for insight in feature_data['insights']:
                created_at = insight.get('created_at', '')
                if created_at:
                    try:
                        year = str(created_at)[:4]
                        if year.isdigit():
                            year_distribution[year] = year_distribution.get(year, 0) + 1
                    except:
                        pass
            
            features_data.append({
                'feature_id': feature_id,
                'feature_name': feature_title,
                'cluster': cluster,
                'insight_count': len(feature_data['insights']),
                'company_count': len(feature_data['companies']),
                'companies': list(feature_data['companies']),
                'sample_quotes': feature_data['sample_texts'][:5],
                'year_distribution': year_distribution,
                'insights': feature_data['insights'],
            })
    
    features_df = pd.DataFrame(features_data)
    
    print(f"✅ Extracted {len(features_df)} features from insights")
    
    # Print summary
    print(f"\n📊 Features per cluster:")
    cluster_summary = features_df.groupby('cluster').agg({
        'feature_id': 'count',
        'insight_count': 'sum',
        'company_count': 'sum'
    }).rename(columns={'feature_id': 'features'})
    
    for cluster, row in cluster_summary.iterrows():
        print(f"   {cluster}: {row['features']} features, {row['insight_count']} insights")
    
    return features_df


def derive_subfeatures(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    For features with many insights, derive sub-features.
    
    Sub-features are more specific aspects of a main feature.
    """
    subfeatures_data = []
    
    for _, feature in features_df.iterrows():
        if feature['insight_count'] < 3:
            # Not enough insights to derive sub-features
            continue
        
        # Group insights by their derived sub-titles
        sub_features = defaultdict(list)
        
        for insight in feature['insights']:
            text = insight.get('cleaned_text', '') or insight.get('note_text', '')
            if text:
                # Try to extract a more specific aspect
                phrases = extract_key_phrases(str(text))
                if phrases:
                    sub_key = phrases[0].title()
                else:
                    sub_key = "General"
                sub_features[sub_key].append(insight)
        
        # Create sub-feature records
        for sub_name, insights in sub_features.items():
            if len(insights) >= 1:
                companies = set()
                for ins in insights:
                    companies.add(ins.get('cleaned_company', 'Unknown'))
                
                subfeatures_data.append({
                    'feature_id': feature['feature_id'],
                    'feature_name': feature['feature_name'],
                    'subfeature_name': sub_name,
                    'cluster': feature['cluster'],
                    'insight_count': len(insights),
                    'company_count': len(companies),
                })
    
    return pd.DataFrame(subfeatures_data)


def get_cluster_summary(classified_df: pd.DataFrame, 
                        features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate cluster summary with insights, features, and companies.
    """
    cluster_data = []
    
    for cluster in classified_df['cluster'].unique():
        cluster_insights = classified_df[classified_df['cluster'] == cluster]
        cluster_features = features_df[features_df['cluster'] == cluster]
        
        # Year-wise breakdown
        year_counts = {}
        if 'created_at' in cluster_insights.columns:
            for _, row in cluster_insights.iterrows():
                created_at = str(row.get('created_at', ''))
                if created_at:
                    year = created_at[:4]
                    if year.isdigit():
                        year_counts[year] = year_counts.get(year, 0) + 1
        
        cluster_data.append({
            'cluster': cluster,
            'total_insights': len(cluster_insights),
            'total_features': len(cluster_features),
            'total_companies': cluster_insights['cleaned_company'].nunique(),
            'avg_insights_per_feature': round(len(cluster_insights) / max(len(cluster_features), 1), 1),
            'year_distribution': year_counts,
        })
    
    return pd.DataFrame(cluster_data)


def get_year_trend_data(classified_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate year-wise trend data for each cluster.
    """
    if 'created_at' not in classified_df.columns:
        return pd.DataFrame()
    
    # Extract year
    df = classified_df.copy()
    df['year'] = pd.to_datetime(df['created_at'], errors='coerce').dt.year
    
    # Group by cluster and year
    trend_data = df.groupby(['cluster', 'year']).agg({
        'insight_id': 'count',
        'cleaned_company': 'nunique'
    }).reset_index()
    
    trend_data.columns = ['cluster', 'year', 'insight_count', 'company_count']
    
    return trend_data


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Feature Extractor Module")
    print("=" * 50)
    
    # Test feature title derivation
    test_insights = [
        ("We need API webhooks to trigger external systems", "APIs"),
        ("Export workflow data via REST API", "APIs"),
        ("Need better audit trail for compliance", "Risk & Compliance"),
        ("Multi-level approval workflow needed", "Asset Lifecycles & Approvals"),
        ("Password reset not working for my account", "Service Ticket"),
        ("Task assignment notifications should go to team", "Case & Task Management"),
    ]
    
    print("\nTest Feature Derivation:")
    print("-" * 50)
    
    for text, cluster in test_insights:
        feature = derive_feature_title(text, cluster)
        print(f"  '{text[:50]}...'")
        print(f"    → Feature: {feature}")
        print()

"""
========================================
DYNAMIC CLUSTER ANALYZER
========================================
Automatically identifies themes/clusters from insight content
using NLP techniques and keyword analysis.

This module analyzes insights to discover natural groupings
without predefined cluster categories.
"""

import pandas as pd
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set
import math


# ============================================================================
# THEME EXTRACTION PATTERNS
# ============================================================================

# Core capability patterns that indicate feature themes
CAPABILITY_PATTERNS = {
    # User & Access Management
    "User Management": [
        r'\b(user)\s*(management|admin|creation|roles?|permission|access)\b',
        r'\b(add|create|remove|delete|manage)\s*(user|member|participant)\b',
        r'\b(role(s)?|permission(s)?|access\s*right(s)?)\b',
        r'\b(SSO|SAML|authentication|login|sign\s*in)\b'
    ],
    "Access Control": [
        r'\b(access)\s*(control|right|permission|level)\b',
        r'\b(restrict|limit)\s*(access|permission|view)\b',
        r'\b(read|write|edit)\s*(access|permission)\b',
        r'\b(folder|workspace)\s*(access|permission)\b'
    ],
    
    # Integration & APIs
    "API & Integration": [
        r'\b(API|REST|web\s*service|endpoint)\b',
        r'\b(integrat(e|ion)|connect(or)?|interfac(e|ing))\b',
        r'\b(webhook|callback|trigger)\b',
        r'\b(SAP|Salesforce|ServiceNow|Jira|SharePoint)\s*(integrat|connect)\b'
    ],
    "Data Import/Export": [
        r'\b(import|export)\s*(data|file|diagram|process)\b',
        r'\b(CSV|Excel|XML|JSON|PDF)\s*(import|export)\b',
        r'\b(bulk|batch)\s*(import|export|upload|download)\b',
        r'\b(migrat(e|ion)|transfer|convert)\b'
    ],
    
    # Workflow & Automation
    "Workflow Automation": [
        r'\b(workflow)\s*(automat|engine|trigger|rule)\b',
        r'\b(automat(e|ion|ic))\s*(workflow|process|task)\b',
        r'\b(trigger|schedule|cron|timer)\b',
        r'\b(rule|condition|logic)\s*(engine|based)\b'
    ],
    "Approval Process": [
        r'\b(approval)\s*(workflow|process|chain|step)\b',
        r'\b(approv(e|al)|reject|review)\s*(process|request|task)\b',
        r'\b(sign\s*off|authorize|validate)\b',
        r'\b(multi|parallel|sequential)\s*(approval|sign)\b'
    ],
    
    # Content & Documentation
    "Process Documentation": [
        r'\b(document(ation)?|describe|detail)\s*(process|workflow)\b',
        r'\b(process)\s*(document|description|definition)\b',
        r'\b(procedure|instruction|guideline|manual)\b',
        r'\b(wiki|knowledge\s*base|help\s*article)\b'
    ],
    "Templates & Standards": [
        r'\b(template|standard|blueprint|reference)\b',
        r'\b(best\s*practice|convention|guideline)\b',
        r'\b(reuse|reusable|library)\b',
        r'\b(pattern|model|framework)\b'
    ],
    
    # UI & Experience
    "User Interface": [
        r'\b(UI|UX|interface|experience)\b',
        r'\b(design|layout|display|view)\b',
        r'\b(dashboard|widget|component|visual)\b',
        r'\b(navigation|menu|tab|panel)\b'
    ],
    "Search & Discovery": [
        r'\b(search|find|discover|locate)\b',
        r'\b(filter|sort|browse|explore)\b',
        r'\b(query|lookup|retrieve)\b',
        r'\b(smart|advanced|full\s*text)\s*(search)\b'
    ],
    
    # Analytics & Reporting
    "Analytics & Dashboards": [
        r'\b(analytic|dashboard|report|metric)\b',
        r'\b(KPI|measure|indicator|scorecard)\b',
        r'\b(chart|graph|visualization|visual)\b',
        r'\b(insight|trend|pattern|analysis)\b'
    ],
    "Process Mining": [
        r'\b(process)\s*(mining|discovery|analysis)\b',
        r'\b(event\s*log|trace|conformance)\b',
        r'\b(variant|deviation|bottleneck)\b',
        r'\b(root\s*cause|optimization|improvement)\b'
    ],
    
    # Collaboration
    "Comments & Feedback": [
        r'\b(comment|feedback|annotation|note)\b',
        r'\b(discuss|conversation|thread|reply)\b',
        r'\b(mention|notify|alert)\b',
        r'\b(@|tag|reference)\s*(user|person|member)\b'
    ],
    "Notifications & Alerts": [
        r'\b(notif(y|ication)|alert|remind(er)?)\b',
        r'\b(email|message|push|inbox)\b',
        r'\b(subscribe|follow|watch|track)\b',
        r'\b(digest|summary|update)\s*(email|notif)\b'
    ],
    
    # Task & Case Management
    "Task Management": [
        r'\b(task)\s*(management|assign|create|track)\b',
        r'\b(assign|delegate|allocate)\s*(task|work|action)\b',
        r'\b(to\s*do|action\s*item|checklist)\b',
        r'\b(due\s*date|deadline|priority|status)\b'
    ],
    "Case Management": [
        r'\b(case)\s*(management|handling|tracking)\b',
        r'\b(case)\s*(create|open|close|resolve)\b',
        r'\b(instance|execution|run)\b',
        r'\b(form|input|data\s*entry|field)\b'
    ],
    
    # Modeling & Design
    "Process Modeling": [
        r'\b(model|diagram|BPMN|map)\b',
        r'\b(process)\s*(model|design|map|flow)\b',
        r'\b(swimlane|pool|lane|shape)\b',
        r'\b(connector|arrow|link|sequence)\b'
    ],
    "Simulation": [
        r'\b(simulat(e|ion)|scenario|what\s*if)\b',
        r'\b(capacity|resource|time)\s*(planning|analysis)\b',
        r'\b(cost|duration|cycle\s*time)\b',
        r'\b(test|validate|verify)\s*(process|model)\b'
    ],
    
    # Governance & Compliance
    "Governance Controls": [
        r'\b(governance|compliance|audit|control)\b',
        r'\b(policy|regulation|standard|rule)\b',
        r'\b(SOX|GDPR|ISO|regulatory)\b',
        r'\b(risk|control|mitigat(e|ion))\b'
    ],
    "Version Control": [
        r'\b(version|revision|history|change)\b',
        r'\b(track|audit|log)\s*(change|modif)\b',
        r'\b(compare|diff|merge|branch)\b',
        r'\b(restore|rollback|revert)\b'
    ],
    
    # Performance & Technical
    "Performance": [
        r'\b(performance|speed|fast|slow|lag)\b',
        r'\b(load|loading|response)\s*(time|speed)\b',
        r'\b(scalab|optimiz|improv)\b',
        r'\b(timeout|error|crash|bug)\b'
    ],
    "Mobile & Offline": [
        r'\b(mobile|tablet|phone|app)\b',
        r'\b(responsive|adaptive|touch)\b',
        r'\b(offline|sync|reconnect)\b',
        r'\b(iOS|Android|native)\b'
    ],
    
    # Multi-language & Localization
    "Localization": [
        r'\b(language|translat(e|ion)|locali[sz])\b',
        r'\b(multi\s*language|multilingual|i18n)\b',
        r'\b(regional|locale|timezone)\b',
        r'\b(german|french|spanish|chinese|japanese)\b'
    ],
    
    # Content Management
    "Content Publishing": [
        r'\b(publish|release|deploy)\b',
        r'\b(preview|draft|staging)\b',
        r'\b(portal|hub|site|page)\b',
        r'\b(widget|embed|iframe)\b'
    ],
    
    # Data & ETL
    "Data Management": [
        r'\b(data)\s*(management|quality|clean|transform)\b',
        r'\b(ETL|pipeline|extraction|load)\b',
        r'\b(database|storage|warehouse)\b',
        r'\b(column|field|attribute|mapping)\b'
    ]
}


def extract_keywords(text: str) -> List[str]:
    """Extract significant keywords from text."""
    if pd.isna(text) or not text:
        return []
    
    # Clean text
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    # Remove short words and common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
        'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here',
        'there', 'then', 'once', 'please', 'like', 'want', 'need', 'able'
    }
    
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    return keywords


def identify_theme(text: str, tags: str = "") -> Tuple[str, float]:
    """
    Identify the primary theme of an insight based on content.
    
    Returns:
        Tuple of (theme_name, confidence_score)
    """
    if pd.isna(text) or not text:
        return ("Other", 0.0)
    
    combined_text = f"{text} {tags}" if tags and not pd.isna(tags) else str(text)
    
    scores = {}
    
    for theme, patterns in CAPABILITY_PATTERNS.items():
        score = 0.0
        for pattern in patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            score += len(matches) * 0.5
        
        if score > 0:
            scores[theme] = score
    
    if not scores:
        return ("Other", 0.0)
    
    # Return theme with highest score
    best_theme = max(scores, key=scores.get)
    max_score = scores[best_theme]
    confidence = min(1.0, max_score / 3.0)
    
    return (best_theme, confidence)


def analyze_themes_for_product(df: pd.DataFrame, product: str = None) -> Dict:
    """
    Analyze themes/clusters for insights of a specific product.
    
    Returns a dictionary with:
    - themes: List of themes with counts
    - theme_insights: Mapping of theme to insight indices
    - top_keywords: Most common keywords
    - year_trend: Theme distribution by year
    """
    print(f"\n🔍 Analyzing themes for {product if product else 'all insights'}...")
    
    # Get text column
    text_col = 'cleaned_text' if 'cleaned_text' in df.columns else 'note_text'
    
    # Identify themes for each insight
    themes = []
    confidences = []
    
    for idx, row in df.iterrows():
        text = row.get(text_col, '')
        tags = row.get('tags', '')
        
        theme, conf = identify_theme(text, tags)
        themes.append(theme)
        confidences.append(conf)
    
    df_analyzed = df.copy()
    df_analyzed['theme'] = themes
    df_analyzed['theme_confidence'] = confidences
    
    # Calculate theme distribution
    theme_counts = df_analyzed['theme'].value_counts()
    total_insights = len(df_analyzed)
    
    theme_data = []
    for theme, count in theme_counts.items():
        pct = (count / total_insights) * 100
        companies = df_analyzed[df_analyzed['theme'] == theme]['cleaned_company'].nunique() \
            if 'cleaned_company' in df_analyzed.columns else 0
        theme_data.append({
            'theme': theme,
            'insight_count': count,
            'percentage': round(pct, 1),
            'company_count': companies
        })
    
    # Top keywords overall
    all_keywords = []
    for text in df[text_col].dropna():
        all_keywords.extend(extract_keywords(str(text)))
    
    keyword_counts = Counter(all_keywords)
    top_keywords = keyword_counts.most_common(30)
    
    # Year trend per theme
    year_trend = []
    if 'created_at' in df_analyzed.columns:
        df_analyzed['year'] = pd.to_datetime(df_analyzed['created_at'], errors='coerce').dt.year
        
        for theme in theme_counts.index:
            theme_df = df_analyzed[df_analyzed['theme'] == theme]
            for year, group in theme_df.groupby('year'):
                if pd.notna(year) and year > 2015:
                    year_trend.append({
                        'theme': theme,
                        'year': int(year),
                        'count': len(group)
                    })
    
    # Company distribution per theme
    company_dist = []
    if 'cleaned_company' in df_analyzed.columns:
        for theme in theme_counts.index:
            theme_df = df_analyzed[df_analyzed['theme'] == theme]
            top_companies = theme_df['cleaned_company'].value_counts().head(10)
            for company, count in top_companies.items():
                if company and pd.notna(company):
                    company_dist.append({
                        'theme': theme,
                        'company': company,
                        'insight_count': count
                    })
    
    print(f"   Found {len(theme_counts)} themes")
    print(f"   Top themes: {', '.join(theme_counts.head(5).index.tolist())}")
    
    return {
        'df': df_analyzed,
        'themes': theme_data,
        'top_keywords': top_keywords,
        'year_trend': pd.DataFrame(year_trend) if year_trend else pd.DataFrame(),
        'company_dist': pd.DataFrame(company_dist) if company_dist else pd.DataFrame()
    }


def derive_features_from_themes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive potential features from themed insights.
    Groups similar insights into feature suggestions.
    """
    text_col = 'cleaned_text' if 'cleaned_text' in df.columns else 'note_text'
    
    features = []
    
    # Group by theme
    for theme, theme_df in df.groupby('theme'):
        if theme == 'Other':
            continue
        
        # Extract common keywords within theme
        theme_keywords = []
        for text in theme_df[text_col].dropna():
            theme_keywords.extend(extract_keywords(str(text)))
        
        keyword_counts = Counter(theme_keywords)
        top_keywords = [kw for kw, _ in keyword_counts.most_common(5)]
        
        # Create feature name from theme and top keywords
        feature_name = f"{theme}: {', '.join(top_keywords[:3])}" if top_keywords else theme
        
        # Count insights and companies
        insight_count = len(theme_df)
        company_count = theme_df['cleaned_company'].nunique() if 'cleaned_company' in theme_df.columns else 0
        
        # Sample quotes (top 3 insights)
        sample_quotes = theme_df[text_col].head(3).tolist()
        sample_companies = theme_df['cleaned_company'].head(3).tolist() if 'cleaned_company' in df.columns else []
        
        features.append({
            'feature_name': feature_name,
            'theme': theme,
            'insight_count': insight_count,
            'company_count': company_count,
            'top_keywords': top_keywords,
            'sample_quotes': sample_quotes,
            'sample_companies': sample_companies
        })
    
    features_df = pd.DataFrame(features)
    
    # Calculate RICE scores
    if len(features_df) > 0:
        max_companies = features_df['company_count'].max() if features_df['company_count'].max() > 0 else 1
        
        features_df['reach'] = features_df['company_count']
        features_df['impact'] = features_df['insight_count'].apply(
            lambda x: min(3.0, 0.5 + (x / 10) * 0.5)
        )
        features_df['confidence'] = features_df.apply(
            lambda row: min(1.0, (row['insight_count'] / 20) + (row['company_count'] / 30)), axis=1
        )
        features_df['effort'] = features_df['theme'].apply(
            lambda t: 5 if t in ['API & Integration', 'Process Mining', 'Workflow Automation'] else 3
        )
        features_df['rice_score'] = (
            features_df['reach'] * 
            features_df['impact'] * 
            features_df['confidence'] / 
            features_df['effort']
        ).round(2)
        
        # Rank features
        features_df = features_df.sort_values('rice_score', ascending=False).reset_index(drop=True)
        features_df['rank'] = features_df.index + 1
    
    return features_df


if __name__ == "__main__":
    # Test the analyzer
    print("Testing dynamic cluster analyzer...")
    
    test_texts = [
        "We need better API integration with Salesforce",
        "Users cannot find processes, search is too slow",
        "Add approval workflow for document publishing",
        "Dashboard should show KPIs and metrics",
        "Mobile app crashes when offline",
        "Need multi-language support for German users",
        "Please unlock my account, forgot password"
    ]
    
    for text in test_texts:
        theme, conf = identify_theme(text)
        print(f"'{text[:50]}...' -> {theme} ({conf:.2f})")

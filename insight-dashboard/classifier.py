"""
========================================
CLASSIFIER MODULE
========================================
This module handles the AI-powered classification of customer insights into
predefined clusters and sub-clusters.

What this module does:
1. Analyzes insight text to determine the best matching cluster
2. Uses keyword matching as a fallback for simple cases
3. Can integrate with AI APIs (OpenAI, etc.) for smarter classification
4. Maps insights to the Feature → Sub-feature hierarchy

Key Concepts for Beginners:
- "Classification" means putting things into categories
- We use "keywords" as hints to determine categories
- "AI classification" uses language models for smarter categorization
- A "confidence score" tells us how sure we are about the classification
"""

import re
from typing import Dict, List, Tuple, Optional
import pandas as pd

# Import our configuration
from config import (
    CLUSTER_DEFINITIONS,
    CLASSIFICATION_KEYWORDS,
    SUBCLUSTER_KEYWORDS,
)


def keyword_match_score(text: str, keywords: List[str]) -> float:
    """
    Calculate how well a text matches a list of keywords.
    
    What it does:
    - Counts how many keywords appear in the text
    - Returns a score from 0.0 (no matches) to 1.0 (all keywords match)
    
    Parameters:
        text: The text to analyze
        keywords: List of keywords to look for
    
    Returns:
        Float score between 0 and 1
    
    Example:
        text = "We need better API integration with webhooks"
        keywords = ["api", "integration", "webhook"]
        score = keyword_match_score(text, keywords)  # Returns ~0.67
    """
    if not text or not keywords:
        return 0.0
    
    text_lower = text.lower()
    matches = 0
    
    for keyword in keywords:
        # Use word boundary matching for more accurate results
        # This prevents "api" from matching "capital"
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matches += 1
    
    # Return proportion of keywords matched
    return matches / len(keywords) if keywords else 0.0


def is_service_ticket(text: str) -> Tuple[bool, float]:
    """
    Check if the text is likely a service/support ticket rather than a feature insight.
    
    Service tickets are operational issues like:
    - Password/login problems
    - Account locked
    - Error messages
    - Things not working
    
    Returns:
        Tuple of (is_service_ticket, confidence)
    """
    if not text:
        return False, 0.0
    
    text_lower = text.lower()
    
    # Strong service ticket indicators (high confidence)
    strong_indicators = [
        r'\b(password|passwd)\b.*(reset|forgot|change|not working|issue)',
        r'\b(account|login)\b.*(locked|blocked|cannot|unable|failed)',
        r'\bcannot (login|log in|access|sign in)\b',
        r'\b(access denied|permission denied)\b',
        r'\berror\b.*(message|code|when|while)',
        r'\b(not working|doesnt work|does not work|broken)\b',
        r'\b(help|urgent|fix|asap)\b.*(please|needed|required)',
        r'\b(locked out|can\'t get in|unable to access)\b',
    ]
    
    for pattern in strong_indicators:
        if re.search(pattern, text_lower):
            return True, 0.85
    
    # Medium service ticket indicators
    medium_indicators = [
        'password', 'login issue', 'account issue', 'cannot access',
        'error message', 'not working', 'please help', 'urgent',
        'locked', 'failed', 'crash', 'bug report'
    ]
    
    matches = sum(1 for ind in medium_indicators if ind in text_lower)
    if matches >= 2:
        return True, 0.7
    elif matches == 1:
        # Check if this looks like a short support request
        if len(text) < 200:
            return True, 0.5
    
    return False, 0.0


def classify_to_cluster(text: str) -> Tuple[str, float]:
    """
    Classify text into one of the main clusters using keyword matching.
    
    What it does:
    - First checks if this is a service ticket (support request)
    - Then checks the text against keywords for each cluster
    - Returns the best matching cluster and a confidence score
    
    Parameters:
        text: The insight text to classify
    
    Returns:
        Tuple of (cluster_name, confidence_score)
    
    Example:
        cluster, confidence = classify_to_cluster("We need better API webhooks")
        # Returns ("APIs", 0.75)
    """
    if not text or len(text.strip()) < 5:
        return "Other Collaboration Features", 0.0
    
    # First, check if this is a service ticket
    is_ticket, ticket_confidence = is_service_ticket(text)
    if is_ticket and ticket_confidence >= 0.5:
        return "Service Ticket", ticket_confidence
    
    best_cluster = "Other Collaboration Features"
    best_score = 0.0
    
    # Check each cluster's keywords (excluding Service Ticket, already checked)
    for cluster, keywords in CLASSIFICATION_KEYWORDS.items():
        if cluster == "Service Ticket":
            continue
        score = keyword_match_score(text, keywords)
        
        if score > best_score:
            best_score = score
            best_cluster = cluster
    
    # If no good match found, default to "Other Collaboration Features"
    if best_score < 0.05:  # Less than 5% match
        return "Other Collaboration Features", 0.1
    
    return best_cluster, min(best_score * 2, 1.0)  # Scale up but cap at 1.0


def classify_to_subcluster(text: str, main_cluster: str) -> Tuple[str, float]:
    """
    Classify text into a sub-cluster within the given main cluster.
    
    What it does:
    - Given the main cluster, finds the best matching sub-cluster
    - Uses more specific keywords for sub-cluster matching
    
    Parameters:
        text: The insight text to classify
        main_cluster: The main cluster this text belongs to
    
    Returns:
        Tuple of (subcluster_name, confidence_score)
    
    Example:
        subcluster, confidence = classify_to_subcluster(
            "Need webhook triggers for external systems",
            "APIs"
        )
        # Returns ("Trigger", 0.8)
    """
    # Get sub-clusters for this main cluster
    subclusters = CLUSTER_DEFINITIONS.get(main_cluster, [])
    
    if not subclusters:
        return "Other", 0.5
    
    # Default to first sub-cluster
    best_subcluster = subclusters[0]
    best_score = 0.0
    
    # Check each sub-cluster's keywords
    for subcluster in subclusters:
        keywords = SUBCLUSTER_KEYWORDS.get(subcluster, [])
        if keywords:
            score = keyword_match_score(text, keywords)
            if score > best_score:
                best_score = score
                best_subcluster = subcluster
    
    # If no good match, use the first sub-cluster with lower confidence
    if best_score < 0.05:
        return subclusters[0], 0.3
    
    return best_subcluster, min(best_score * 2, 1.0)


def classify_insight(text: str) -> Dict:
    """
    Perform complete classification of an insight.
    
    This is the main function to use for classifying a single insight.
    It determines both the main cluster and sub-cluster.
    
    Parameters:
        text: The insight text to classify
    
    Returns:
        Dictionary with classification results:
        {
            'cluster': 'Main cluster name',
            'subcluster': 'Sub-cluster name',
            'cluster_confidence': 0.0-1.0,
            'subcluster_confidence': 0.0-1.0,
            'overall_confidence': 0.0-1.0
        }
    
    Example:
        result = classify_insight("We need API webhooks for our CRM")
        print(result['cluster'])     # "APIs"
        print(result['subcluster'])  # "Trigger"
    """
    # Step 1: Classify to main cluster
    cluster, cluster_confidence = classify_to_cluster(text)
    
    # Step 2: Classify to sub-cluster within that cluster
    subcluster, subcluster_confidence = classify_to_subcluster(text, cluster)
    
    # Step 3: Calculate overall confidence (average of both)
    overall_confidence = (cluster_confidence + subcluster_confidence) / 2
    
    return {
        'cluster': cluster,
        'subcluster': subcluster,
        'cluster_confidence': round(cluster_confidence, 3),
        'subcluster_confidence': round(subcluster_confidence, 3),
        'overall_confidence': round(overall_confidence, 3),
    }


def classify_all_insights(df: pd.DataFrame, 
                         text_column: str = 'cleaned_text') -> pd.DataFrame:
    """
    Classify all insights in a DataFrame.
    
    This processes each insight and adds classification columns.
    
    Parameters:
        df: DataFrame with insights
        text_column: Name of column containing insight text
    
    Returns:
        DataFrame with new classification columns added:
        - cluster
        - subcluster
        - cluster_confidence
        - subcluster_confidence
        - overall_confidence
    
    Example:
        classified_df = classify_all_insights(prepared_df)
        print(classified_df['cluster'].value_counts())
    """
    print("\n🤖 Classifying insights into clusters...")
    
    # Make a copy
    df_classified = df.copy()
    
    # Initialize new columns
    df_classified['cluster'] = ''
    df_classified['subcluster'] = ''
    df_classified['cluster_confidence'] = 0.0
    df_classified['subcluster_confidence'] = 0.0
    df_classified['overall_confidence'] = 0.0
    
    # Process each insight
    total = len(df_classified)
    for idx, row in df_classified.iterrows():
        text = row[text_column] if pd.notna(row[text_column]) else ""
        
        # Classify
        result = classify_insight(text)
        
        # Store results
        df_classified.at[idx, 'cluster'] = result['cluster']
        df_classified.at[idx, 'subcluster'] = result['subcluster']
        df_classified.at[idx, 'cluster_confidence'] = result['cluster_confidence']
        df_classified.at[idx, 'subcluster_confidence'] = result['subcluster_confidence']
        df_classified.at[idx, 'overall_confidence'] = result['overall_confidence']
        
        # Progress indicator (every 100 insights)
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{total} insights...")
    
    # Print summary
    print(f"\n✅ Classification complete!")
    print(f"\n📊 Distribution by cluster:")
    cluster_counts = df_classified['cluster'].value_counts()
    for cluster, count in cluster_counts.items():
        percentage = (count / total) * 100
        print(f"   {cluster}: {count} ({percentage:.1f}%)")
    
    return df_classified


def get_feature_hierarchy(df_classified: pd.DataFrame) -> Dict:
    """
    Create the Feature → Sub-feature hierarchy from classified insights.
    
    This maps:
    - Main clusters → Features
    - Sub-clusters → Sub-features
    - Each insight → one Sub-feature
    
    Parameters:
        df_classified: DataFrame with classification columns
    
    Returns:
        Dictionary with the complete hierarchy:
        {
            'FeatureName': {
                'insights': [...],
                'subfeatures': {
                    'SubfeatureName': {
                        'insights': [...],
                        'companies': ['Company1', 'Company2']
                    }
                },
                'companies': set()
            }
        }
    """
    hierarchy = {}
    
    for _, row in df_classified.iterrows():
        cluster = row['cluster']
        subcluster = row['subcluster']
        company = row.get('cleaned_company', row.get('company_name', 'Unknown'))
        
        # Create feature entry if doesn't exist
        if cluster not in hierarchy:
            hierarchy[cluster] = {
                'insights': [],
                'subfeatures': {},
                'companies': set()
            }
        
        # Add insight to feature
        hierarchy[cluster]['insights'].append(row.to_dict())
        hierarchy[cluster]['companies'].add(company)
        
        # Create subfeature entry if doesn't exist
        if subcluster not in hierarchy[cluster]['subfeatures']:
            hierarchy[cluster]['subfeatures'][subcluster] = {
                'insights': [],
                'companies': set()
            }
        
        # Add insight to subfeature
        hierarchy[cluster]['subfeatures'][subcluster]['insights'].append(row.to_dict())
        hierarchy[cluster]['subfeatures'][subcluster]['companies'].add(company)
    
    return hierarchy


def get_classification_summary(df_classified: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary table of classifications.
    
    Parameters:
        df_classified: DataFrame with classification columns
    
    Returns:
        Summary DataFrame with counts by cluster and subcluster
    """
    summary = df_classified.groupby(['cluster', 'subcluster']).agg({
        'insight_id': 'count',
        'cleaned_company': 'nunique',
        'overall_confidence': 'mean'
    }).reset_index()
    
    summary.columns = ['Cluster', 'Sub-cluster', 'Insight Count', 
                       'Unique Companies', 'Avg Confidence']
    
    return summary.sort_values(['Cluster', 'Insight Count'], 
                               ascending=[True, False])


# ============================================================================
# AI-POWERED CLASSIFICATION (Optional Enhancement)
# ============================================================================
# This section shows how to integrate with AI APIs for smarter classification.
# Uncomment and configure if you have an OpenAI API key.

"""
import openai

def classify_with_ai(text: str, api_key: str) -> Dict:
    '''
    Use OpenAI's GPT to classify insights more accurately.
    
    This provides much better classification than keyword matching,
    but requires an API key and has a cost per request.
    '''
    openai.api_key = api_key
    
    # Create the prompt
    clusters_str = ', '.join(CLUSTER_DEFINITIONS.keys())
    
    prompt = f'''
    Classify the following customer feedback into one of these categories:
    {clusters_str}
    
    Feedback: "{text}"
    
    Respond with only the category name.
    '''
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    
    cluster = response.choices[0].message.content.strip()
    
    # Validate it's a real cluster
    if cluster not in CLUSTER_DEFINITIONS:
        cluster = "Other Collaboration Features"
    
    return classify_insight(text)  # Still use local for subclusters
"""


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Classifier Module")
    print("=" * 50)
    
    # Test insights
    test_insights = [
        "We need API webhooks to trigger external systems when workflow completes",
        "GDPR compliance is critical - we need better data handling controls",
        "The approval workflow needs to support multiple levels of sign-off",
        "Can we get better cloud migration tools for moving our data?",
        "AI-powered recommendations would help users complete tasks faster",
        "Task assignment notifications should go to the whole team",
    ]
    
    print("\nTest Classifications:")
    print("-" * 50)
    
    for insight in test_insights:
        result = classify_insight(insight)
        print(f"\n📝 '{insight[:60]}...'")
        print(f"   → Cluster: {result['cluster']} ({result['cluster_confidence']:.0%})")
        print(f"   → Sub-cluster: {result['subcluster']} ({result['subcluster_confidence']:.0%})")

"""
AEO Diagnostic Tool - AI Visibility Checker
Main Streamlit application for checking brand visibility across AI models.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from threading import Thread
import time

from llm_client import query_all_llms
from parser import parse_response, find_target_brand, extract_competitors
from scorer import score_brand_position, calculate_overall_score, score_to_grade, get_grade_description, generate_recommendation

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AEO Diagnostic",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .grade-a { color: #28a745; font-size: 72px; font-weight: bold; }
    .grade-b { color: #28a745; font-size: 72px; font-weight: bold; }
    .grade-c { color: #ffc107; font-size: 72px; font-weight: bold; }
    .grade-d { color: #dc3545; font-size: 72px; font-weight: bold; }
    .grade-f { color: #dc3545; font-size: 72px; font-weight: bold; }
    .metric-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔍 AEO Diagnostic — AI Visibility Checker")
st.markdown("""
Discover how your brand ranks across AI models. This tool queries three leading AI engines 
(Groq, Google Gemini, and Cohere) to analyze your product's visibility and competitive positioning.
""")

st.markdown("---")

# Sidebar for information
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.markdown("""
    **What it does:**
    - Queries 3 AI models simultaneously
    - Ranks your brand's visibility
    - Identifies top competitors
    - Provides actionable recommendations
    
    **How scoring works:**
    - **#1 ranking** → 10 points
    - **#2 ranking** → 8 points
    - **#3 ranking** → 6 points
    - **#4 ranking** → 4 points
    - **#5 ranking** → 2 points
    - **Not mentioned** → 0 points
    
    **Grades:**
    - **A (9-10)** - Excellent visibility
    - **B (7-8)** - Good visibility
    - **C (5-6)** - Moderate visibility
    - **D (3-4)** - Poor visibility
    - **F (0-2)** - Not visible
    """)

# Main input section
col1, col2 = st.columns(2)

with col1:
    user_query = st.text_input(
        "Enter your product query",
        placeholder="best magnesium supplement for seniors",
        help="Describe the product category you want to analyze"
    )

with col2:
    target_brand = st.text_input(
        "Enter your brand name (optional)",
        placeholder="Nature Made",
        help="Your brand name to track in the results"
    )

# Run diagnostic button
if st.button("🚀 Run Diagnostic", use_container_width=True):
    if not user_query:
        st.error("Please enter a product query to continue.")
    else:
        # Show progress
        with st.spinner("🔄 Querying 3 AI engines... This may take 30-60 seconds."):
            # Query all LLMs
            llm_results = query_all_llms(user_query)
        
        # Parse responses
        all_brands = {}
        all_positions = {}
        all_scores = {}
        
        for llm_name, response in llm_results.items():
            brands = parse_response(response)
            all_brands[llm_name] = brands
            
            position, rank_str = find_target_brand(brands, target_brand)
            all_positions[llm_name] = (position, rank_str)
            
            score = score_brand_position(position)
            all_scores[llm_name] = score
        
        # Calculate overall score
        overall_score = calculate_overall_score(list(all_scores.values()))
        grade, color = score_to_grade(overall_score)
        grade_description = get_grade_description(overall_score)
        recommendation = generate_recommendation(overall_score)
        
        # Extract competitors
        all_brands_list = list(all_brands.values())
        competitors = extract_competitors(all_brands_list, target_brand)
        
        # Display results
        st.markdown("---")
        st.header("📊 Diagnostic Results")
        
        # Section 1: Header with overall grade
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"### Query")
            st.markdown(f"*{user_query}*")
        
        with col2:
            st.markdown(f"### Target Brand")
            if target_brand:
                st.markdown(f"**{target_brand}**")
            else:
                st.markdown("*Not specified*")
        
        with col3:
            st.markdown(f"### Overall Grade")
            if grade in ['A', 'B']:
                st.markdown(f'<div class="grade-{grade.lower()}">{grade}</div>', unsafe_allow_html=True)
            elif grade == 'C':
                st.markdown(f'<div class="grade-c">{grade}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="grade-{grade.lower()}">{grade}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Section 2: Overall score display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Overall Visibility Score",
                value=f"{overall_score:.1f}/10",
                delta=grade_description
            )
        
        with col2:
            st.metric(
                label="Grade",
                value=grade,
                delta=f"{grade_description}"
            )
        
        with col3:
            avg_rank = "N/A"
            valid_positions = [p for p, _ in all_positions.values() if p is not None]
            if valid_positions:
                avg_rank = f"#{sum(valid_positions) / len(valid_positions):.1f}"
            st.metric(
                label="Average Rank",
                value=avg_rank
            )
        
        st.markdown("---")
        
        # Section 3: Per-LLM breakdown
        st.subheader("📈 Per-LLM Breakdown")
        
        breakdown_data = []
        for llm_name in all_scores.keys():
            position, rank_str = all_positions[llm_name]
            score = all_scores[llm_name]
            breakdown_data.append({
                "LLM": llm_name,
                "Rank": rank_str,
                "Score": f"{score}/10"
            })
        
        st.table(breakdown_data)
        
        st.markdown("---")
        
        # Section 4: Top competitors
        st.subheader("🏆 Top Competitors")
        
        if competitors:
            competitor_text = ""
            for idx, (brand, freq) in enumerate(competitors[:10], 1):
                competitor_text += f"{idx}. **{brand}** (mentioned {freq}x)\n"
            st.markdown(competitor_text)
        else:
            st.info("No competitor data available.")
        
        st.markdown("---")
        
        # Section 5: Recommendations
        st.subheader("💡 Recommendations")
        
        if overall_score < 5:
            st.error(recommendation)
        elif overall_score <= 7:
            st.warning(recommendation)
        else:
            st.success(recommendation)
        
        st.markdown("---")
        
        # Section 6: Raw responses (expandable)
        with st.expander("📋 View Raw LLM Responses"):
            for llm_name, response in llm_results.items():
                st.subheader(f"{llm_name} Response")
                st.text(response)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    AEO Diagnostic Tool | Powered by Groq, Google Gemini, and Cohere
</div>
""", unsafe_allow_html=True)

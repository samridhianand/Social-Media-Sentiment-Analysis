import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import re

# Page configuration
st.set_page_config(
    page_title="Social Media Sentiment Analyzer",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .sentiment-positive {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💬 Social Media Sentiment Analyzer")
st.markdown("### Analyze the sentiment of your social media posts in real-time")

# Sidebar
with st.sidebar:
    st.header("📊 About")
    st.info("""
    This app analyzes the sentiment of text using natural language processing.
    
    **Sentiment Categories:**
    - 😊 Positive
    - 😐 Neutral
    - 😢 Negative
    
    **How it works:**
    1. Enter your text
    2. Click 'Analyze Sentiment'
    3. Get instant results!
    """)
    
    st.header("🎯 Example Texts")
    if st.button("Example 1: Positive"):
        st.session_state.example_text = "I absolutely love this product! It's amazing and exceeded all my expectations. Best purchase ever!"
    if st.button("Example 2: Negative"):
        st.session_state.example_text = "This is terrible. Very disappointed with the quality. Would not recommend to anyone."
    if st.button("Example 3: Neutral"):
        st.session_state.example_text = "The product arrived on time. It has the basic features mentioned in the description."

# Function to clean text
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()

# Function to analyze sentiment
def analyze_sentiment(text):
    if not text.strip():
        return None
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = "Positive"
        emoji = "😊"
        color = "#28a745"
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😢"
        color = "#dc3545"
    else:
        sentiment = "Neutral"
        emoji = "😐"
        color = "#ffc107"
    
    confidence = abs(polarity)
    
    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "color": color,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "confidence": confidence
    }

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Text input
    default_text = st.session_state.get('example_text', '')
    user_text = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Type or paste your social media post, comment, or any text you want to analyze...",
        value=default_text
    )
    
    # Clear example text after use
    if 'example_text' in st.session_state:
        del st.session_state.example_text
    
    # Analyze button
    analyze_button = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)
    
    if analyze_button and user_text:
        with st.spinner("Analyzing..."):
            result = analyze_sentiment(user_text)
            
            if result:
                st.markdown("---")
                st.subheader("📈 Analysis Results")
                
                # Display sentiment with custom styling
                sentiment_class = f"sentiment-{result['sentiment'].lower()}"
                st.markdown(f"""
                    <div class="{sentiment_class}">
                        <h2>{result['emoji']} Sentiment: {result['sentiment']}</h2>
                        <p><strong>Polarity Score:</strong> {result['polarity']:.3f} (-1 to 1 scale)</p>
                        <p><strong>Subjectivity:</strong> {result['subjectivity']:.3f} (0 to 1 scale)</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Sentiment", result['sentiment'])
                with col_m2:
                    st.metric("Polarity", f"{result['polarity']:.3f}")
                with col_m3:
                    st.metric("Subjectivity", f"{result['subjectivity']:.3f}")
                
                # Visualizations
                st.markdown("### 📊 Visual Analysis")
                
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    # Polarity gauge
                    fig_polarity = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = result['polarity'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Polarity Score"},
                        gauge = {
                            'axis': {'range': [-1, 1]},
                            'bar': {'color': result['color']},
                            'steps': [
                                {'range': [-1, -0.1], 'color': "lightcoral"},
                                {'range': [-0.1, 0.1], 'color': "lightyellow"},
                                {'range': [0.1, 1], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': result['polarity']
                            }
                        }
                    ))
                    fig_polarity.update_layout(height=300)
                    st.plotly_chart(fig_polarity, use_container_width=True)
                
                with viz_col2:
                    # Subjectivity gauge
                    fig_subjectivity = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = result['subjectivity'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Subjectivity Score"},
                        gauge = {
                            'axis': {'range': [0, 1]},
                            'bar': {'color': "lightblue"},
                            'steps': [
                                {'range': [0, 0.5], 'color': "lightgray"},
                                {'range': [0.5, 1], 'color': "lightsteelblue"}
                            ],
                            'threshold': {
                                'line': {'color': "blue", 'width': 4},
                                'thickness': 0.75,
                                'value': result['subjectivity']
                            }
                        }
                    ))
                    fig_subjectivity.update_layout(height=300)
                    st.plotly_chart(fig_subjectivity, use_container_width=True)
                
                # Interpretation
                st.markdown("### 💡 Interpretation")
                
                # Polarity interpretation
                if result['polarity'] > 0.5:
                    polarity_text = "Very Positive - The text expresses strong positive emotions"
                elif result['polarity'] > 0.1:
                    polarity_text = "Positive - The text has a generally positive tone"
                elif result['polarity'] > -0.1:
                    polarity_text = "Neutral - The text is balanced or factual"
                elif result['polarity'] > -0.5:
                    polarity_text = "Negative - The text has a generally negative tone"
                else:
                    polarity_text = "Very Negative - The text expresses strong negative emotions"
                
                # Subjectivity interpretation
                if result['subjectivity'] > 0.6:
                    subjectivity_text = "Highly Subjective - Personal opinions and emotions dominate"
                elif result['subjectivity'] > 0.3:
                    subjectivity_text = "Moderately Subjective - Mix of facts and opinions"
                else:
                    subjectivity_text = "Objective - Mostly factual information"
                
                st.info(f"**Polarity:** {polarity_text}")
                st.info(f"**Subjectivity:** {subjectivity_text}")
    
    elif analyze_button:
        st.warning("⚠️ Please enter some text to analyze!")

with col2:
    st.markdown("### 📝 Quick Guide")
    st.markdown("""
    **Polarity** measures sentiment:
    - **+1.0**: Very Positive
    - **0.0**: Neutral
    - **-1.0**: Very Negative
    
    **Subjectivity** measures opinion vs fact:
    - **1.0**: Very Subjective (opinions)
    - **0.0**: Very Objective (facts)
    """)
    
    st.markdown("---")
    st.markdown("### 🎨 Sentiment Distribution")
    
    # Sample data visualization
    sample_data = pd.DataFrame({
        'Sentiment': ['Positive', 'Neutral', 'Negative'],
        'Count': [45, 30, 25]
    })
    
    fig_pie = px.pie(
        sample_data, 
        values='Count', 
        names='Sentiment',
        color='Sentiment',
        color_discrete_map={
            'Positive': '#28a745',
            'Neutral': '#ffc107',
            'Negative': '#dc3545'
        },
        hole=0.4
    )
    fig_pie.update_layout(height=300)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.caption("Sample sentiment distribution")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        
    </div>
""", unsafe_allow_html=True)

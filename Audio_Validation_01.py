# streamlit_app.py
import streamlit as st
import pandas as pd
from datasets import load_from_disk, Audio
import plotly.express as px
import plotly.graph_objects as go


DATASET_PATH = "CV-17-01/validated"
CSV_PATH = "results_no_audio_preprocessing.csv"
TARGET_SR = 16000


st.set_page_config(
    page_title="Whisper Evaluation Explorer", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎧"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: #0a0a0f;
        color: #e4e4e7;
    }
    
    .main {
        background: #0a0a0f;
        padding: 0rem 1rem;
    }
    
    /* Main Header - Cyberpunk Style */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 2px solid #00d4aa;
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        color: #ffffff;
        text-align: center;
        box-shadow: 
            0 0 40px rgba(0, 212, 170, 0.3),
            inset 0 0 40px rgba(0, 212, 170, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #00d4aa, #00a8ff, #8c7ae6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 1rem;
        color: #a0aec0;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #2d3748;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 10px 40px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00d4aa, #00a8ff, #8c7ae6);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.7),
            0 0 30px rgba(0, 212, 170, 0.3);
        border-color: #00d4aa;
    }
    
    .metric-card h4 {
        color: #00d4aa;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Section Headers - Neon Style */
    .section-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #00d4aa;
        color: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1.4rem;
        box-shadow: 
            0 0 30px rgba(0, 212, 170, 0.3),
            inset 0 1px 0 rgba(0, 212, 170, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .audio-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        border: 1px solid #00a8ff;
        color: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1.4rem;
        box-shadow: 
            0 0 30px rgba(0, 168, 255, 0.3),
            inset 0 1px 0 rgba(0, 168, 255, 0.2);
    }
    
    .quick-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%);
        border: 1px solid #8c7ae6;
        color: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1.4rem;
        box-shadow: 
            0 0 30px rgba(140, 122, 230, 0.3),
            inset 0 1px 0 rgba(140, 122, 230, 0.2);
    }
    
    /* Sample Cards - Glassmorphism */
    .sample-card {
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .sample-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4aa, transparent);
    }
    
    .sample-card:hover {
        border-color: rgba(0, 212, 170, 0.5);
        box-shadow: 
            0 16px 48px rgba(0,0,0,0.4),
            0 0 30px rgba(0, 212, 170, 0.2);
        transform: translateY(-5px);
    }
    
    .sample-card h4 {
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    /* WER Badges - Neon */
    .wer-badge {
        background: linear-gradient(135deg, #00d4aa 0%, #00a8ff 100%);
        color: #0a0a0f;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 20px rgba(0, 212, 170, 0.5),
            inset 0 1px 0 rgba(255,255,255,0.3);
        text-shadow: none;
        font-size: 0.9rem;
    }
    
    .wer-badge-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Text Containers - Dark Theme */
    .text-prediction {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        color: #e4e4e7;
        box-shadow: inset 0 1px 0 rgba(59, 130, 246, 0.1);
    }
    
    .text-reference {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        color: #e4e4e7;
        box-shadow: inset 0 1px 0 rgba(34, 197, 94, 0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
    }
    
    /* Button Styling - Cyberpunk */
    .stButton button {
        background: linear-gradient(135deg, #00d4aa 0%, #00a8ff 100%);
        color: #0a0a0f;
        border: none;
        border-radius: 16px;
        padding: 1rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 20px rgba(0, 212, 170, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 8px 30px rgba(0, 212, 170, 0.6),
            0 0 30px rgba(0, 212, 170, 0.4);
    }
    
    /* Slider Styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00d4aa, #00a8ff) !important;
    }
    
    /* Input Styling */
    .stTextInput input {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
        color: #e4e4e7 !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #00d4aa !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3) !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(26, 26, 46, 0.8) !important;
        border-radius: 16px !important;
        border: 1px solid #2d3748 !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #22c55e !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #f59e0b !important;
    }
    
    /* Metrics Styling */
    .metric-container {
        background: rgba(26, 26, 46, 0.6) !important;
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Audio Player Styling */
    audio {
        width: 100%;
        border-radius: 12px;
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #2d3748;
    }
    
    /* RTL Text */
    .rtl-text {
        direction: rtl;
        text-align: right;
        color: #a0aec0;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00d4aa, #00a8ff);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00a8ff, #8c7ae6);
    }
    
    /* Animated Divider */
    .neon-divider {
        margin: 3rem 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4aa, #00a8ff, #8c7ae6, transparent);
        border-radius: 1px;
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { opacity: 0.4; }
        to { opacity: 1; }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 3px solid rgba(0, 212, 170, 0.3);
        border-top: 3px solid #00d4aa;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_dataset():
    dataset = load_from_disk(DATASET_PATH)
    dataset = dataset.cast_column("audio", Audio(sampling_rate=TARGET_SR))
    return dataset

@st.cache_data
def load_csv():
    return pd.read_csv(CSV_PATH)

with st.spinner('Loading dataset...'):
    full_dataset = load_dataset()
    df = load_csv()


st.markdown("""
<div class="main-header">
    <h1>🎧 Whisper Evaluation Dashboard</h1>
    <p>An advanced, dark-themed environment to explore model predictions, compare with references, and listen to audio.</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### 📈 Overall Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total Samples",
            value=f"{len(df):,}",
            delta=None
        )
    with col2:
        st.metric(
            label="Average WER",
            value=f"{df['wer_normalized'].mean():.3f}",
            delta=f"±{df['wer_normalized'].std():.3f}"
        )
    
    fig = px.histogram(
        df, 
        x="wer_normalized", 
        nbins=50, 
        title="WER Distribution",
        color_discrete_sequence=['#00d4aa']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10, color='#e4e4e7'),
        title_font_color='#00d4aa',
        height=300,
        xaxis=dict(gridcolor='#2d3748'),
        yaxis=dict(gridcolor='#2d3748')
    )
    st.plotly_chart(fig, use_container_width=True)


st.markdown('<div class="section-header">📊 CSV Results & Smart Filters</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    min_wer, max_wer = st.slider(
        "🎯 Select WER_normalized range:",
        float(df["wer_normalized"].min()),
        float(df["wer_normalized"].max()),
        (float(df["wer_normalized"].min()), float(df["wer_normalized"].max())),
        step=0.01,
        help="Samples with WER in this range will be displayed"
    )

with col2:
    sort_column = st.selectbox(
        "🔄 Sort by:",
        ["wer_normalized", "original_index"],
        help="Column to sort by"
    )

with col3:
    ascending = st.checkbox(
        "Ascending",
        value=True,
        help="Ascending or descending order"
    )

filtered_df = df[
    (df["wer_normalized"] >= min_wer) & (df["wer_normalized"] <= max_wer)
]


st.markdown(f"""
<div class="metric-card">
    <h4>📈 Filtered Statistics</h4>
    <p><strong>Filtered Samples:</strong> <span style="color: #00d4aa;">{len(filtered_df):,}</span> of {len(df):,}</p>
    <p><strong>Filtered Average WER:</strong> <span style="color: #00a8ff;">{filtered_df['wer_normalized'].mean():.3f}</span></p>
    <p><strong>Min WER:</strong> <span style="color: #22c55e;">{filtered_df['wer_normalized'].min():.3f}</span> | 
        <strong>Max WER:</strong> <span style="color: #ef4444;">{filtered_df['wer_normalized'].max():.3f}</span></p>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df.sort_values(sort_column, ascending=ascending),
    use_container_width=True,
    hide_index=True,
    height=400
)


st.markdown('<div class="audio-section">🎶 Audio Player by original_index</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    indices_input = st.text_input(
        "🎵 Enter index/indices (comma-separated):", 
        "159173",
        help="Example: 159173,123456,789012"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎧 Play Audio", type="primary"):
        st.rerun()

if indices_input:
    try:
        indices = [int(x.strip()) for x in indices_input.split(",")]
        
        with st.spinner('Loading audio files...'):
            for i, idx in enumerate(indices):
                if 0 <= idx < len(full_dataset):
                    sample = full_dataset[idx]
                    audio_data = sample["audio"]
                    reference_text = sample["sentence"]
                    

                    csv_row = df[df["original_index"] == idx]
                    wer_info = ""
                    prediction_text = ""
                    wer_class = "wer-badge"
                    
                    if not csv_row.empty:
                        wer_score = csv_row.iloc[0]["wer_normalized"]
                        prediction_text = csv_row.iloc[0]["prediction_normalized"]
                        if wer_score > 0.5:
                            wer_class = "wer-badge wer-badge-high"
                        wer_info = f'<span class="{wer_class}">WER: {wer_score:.3f}</span>'

                    st.markdown(f"""
                    <div class="sample-card">
                        <h4>🎵 Sample {i+1} - Index: {idx}</h4>
                        {wer_info}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if prediction_text:
                        st.markdown(f"""
                        <div class="text-prediction">
                            <strong>🤖 Prediction:</strong><br>{prediction_text}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="text-reference">
                        <strong>📄 Reference:</strong><br>{reference_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.audio(audio_data["array"], format="audio/wav", sample_rate=audio_data["sampling_rate"])
                    
                    if i < len(indices) - 1:
                        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Index {idx} is out of the dataset range.")
                    
    except ValueError:
        st.error("❌ Please enter only numbers or a list of numbers.")


st.markdown('<div class="quick-section">⚡ Quick Selection by WER</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    sort_order = st.selectbox(
        "📊 Select WER_normalized sort order:",
        ["Lowest", "Highest"],
        help="Samples with the lowest or highest WER"
    )

with col2:
    top_n = st.number_input(
        "🔢 How many samples?",
        min_value=1,
        max_value=min(20, len(filtered_df)),
        value=5,
        step=1,
        help="Number of samples to display"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    show_samples_btn = st.button("🚀 Show Samples", type="primary")

if show_samples_btn:
    with st.spinner('Processing samples...'):
        if sort_order == "Lowest":
            selected_samples = filtered_df.sort_values("wer_normalized", ascending=True).head(top_n)
            st.success(f"🎯 Displaying {top_n} samples with the lowest WER")
        else:  # Highest
            selected_samples = filtered_df.sort_values("wer_normalized", ascending=False).head(top_n)
            st.warning(f"⚠️ Displaying {top_n} samples with the highest WER")

        for i, (_, row) in enumerate(selected_samples.iterrows()):
            idx = int(row["original_index"])
            if 0 <= idx < len(full_dataset):
                sample = full_dataset[idx]
                audio_data = sample["audio"]
                reference_text = sample["sentence"]

                wer_class = "wer-badge"
                if row['wer_normalized'] > 0.5:
                    wer_class = "wer-badge wer-badge-high"

                st.markdown(f"""
                <div class="sample-card">
                    <h4>🎵 Sample {i+1} - Index: {idx}</h4>
                    <span class="{wer_class}">WER: {row['wer_normalized']:.3f}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="text-prediction">
                    <strong>🤖 Prediction:</strong><br>{row['prediction_normalized']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="text-reference">
                    <strong>📄 Reference:</strong><br>{row['reference_normalized']}
                </div>
                """, unsafe_allow_html=True)
                
                st.audio(audio_data["array"], format="audio/wav", sample_rate=audio_data["sampling_rate"])
                
                if i < len(selected_samples) - 1:
                    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)


st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; text-align: center; 
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
            border-radius: 20px; border: 1px solid #2d3748;">
    <p style="color: #a0aec0; font-size: 1rem;">
        🎧 <strong style="color: #00d4aa;">Whisper Evaluation Dashboard</strong> - Designed for detailed analysis of speech recognition models
    </p>

</div>
""", unsafe_allow_html=True)
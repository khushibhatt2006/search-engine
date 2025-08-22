import streamlit as st
from backend.search_engine import search
import os
from dotenv import load_dotenv

# Page settings
st.set_page_config(page_title="Nova", layout="wide")

# Inject custom CSS + stars
st.markdown("""
    <style>
    /* Full dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0d1b2a, #1b263b, #0d1b2a) !important;
        color: #ffffff !important;
        overflow: hidden; /* prevent scrollbars */
    }

    /* Star container */
    .stars {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -1;
        overflow: hidden;
    }

    /* Individual stars */
    .star {
        position: absolute;
        width: 2px;
        height: 2px;
        background: white;
        border-radius: 50%;
        animation: twinkle 2s infinite ease-in-out alternate,
                   drift 60s linear infinite;
        opacity: 0.8;
    }

    /* Twinkle effect */
    @keyframes twinkle {
        from { opacity: 0.3; transform: scale(1); }
        to { opacity: 1; transform: scale(1.3); }
    }

    /* Slow diagonal drift */
    @keyframes drift {
        from { transform: translate(0, 0); }
        to { transform: translate(50px, 50px); }
    }

    /* Clean NovaSeek Title */
    .title-text {
        font-size: 3rem;
        font-weight: bold;
        color: #00e5ff;
        text-align: center;
        margin-top: 20px;
    }

    /* Search Bar */
    .stTextInput > div > div > input {
        background: #1b263b !important;
        border: 2px solid #00e5ff !important;
        color: #ffffff !important;
        padding: 12px 20px !important;
        border-radius: 25px !important;
        font-size: 1rem !important;
        box-shadow: 0 0 10px #00e5ff40 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #aaaaaa !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        color: #bbbbbb !important;
        font-size: 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00e5ff !important;
        border-bottom: 2px solid #00e5ff !important;
    }

    /* Results Box */
    .results-box {
        background: #0f172a;
        padding: 20px;
        border-radius: 15px;
        margin: 20px auto;
        width: 80%;
        box-shadow: 0 0 20px #00000080;
    }
    </style>
""", unsafe_allow_html=True)

# Add stars HTML
st.markdown(
    '<div class="stars">' +
    "".join([
        f'<div class="star" style="top:{(i*37)%100}vh; left:{(i*73)%100}vw; animation-delay:{i*0.4}s;"></div>'
        for i in range(80)
    ]) +
    '</div>',
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title-text">🔭 Nova</div>', unsafe_allow_html=True)

# Load .env keys
load_dotenv()

# Search box
query = st.text_input(" ", placeholder="Type anything... 🔍")

# Tabs
tab_all, tab_images, tab_news = st.tabs(["All", "Images", "News"])

if query:
    data = search(query)

    # --- ALL Tab ---
    with tab_all:
        results = data["all"]
        if results:
            summary = results[0]
            if summary["title"] == "AI Summary":
                st.markdown(f"""
                <div class="snippet-box">
                    <div class="snippet-title">AI Summary</div>
                    <div class="snippet-text">{summary['snippet']}</div>
                </div>
                """, unsafe_allow_html=True)

                for r in results[1:]:
                    st.markdown(f"""
                    <div style="margin-bottom:15px;">
                        <a class="result-title" href="{r['url']}" target="_blank">{r['title']}</a><br>
                        <div class="result-link">{r['url']}</div>
                        <div class="result-snippet">{r['snippet']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # --- IMAGES Tab ---
    with tab_images:
        images = data["images"]
        if images:
            st.markdown("<div class='image-grid'>", unsafe_allow_html=True)
            for img in images:
                st.markdown(f"""
                <div class="image-box">
                    <a href="{img['url']}" target="_blank">
                        <img src="{img['url']}" alt="{img['title']}"/>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No images found.")

    # --- NEWS Tab ---
    with tab_news:
        news = data["news"]
        if news:
            for n in news:
                st.markdown(f"""
                <div style="margin-bottom:15px;">
                    <a class="result-title" href="{n['url']}" target="_blank">{n['title']}</a><br>
                    <div class="result-snippet">{n['snippet']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No news results found.")

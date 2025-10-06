import streamlit as st
from exa_py import Exa
import os 

# ---------- SETUP ----------
st.set_page_config(page_title="Multi-Site Search Tool", page_icon="🌸", layout="centered")

# Initialize Exa client
EXA_API_KEY = os.environ["EXA_API_KEY"]
exa = Exa(EXA_API_KEY)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #ffe6f0;
    color: #4d0033;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    color: #ff1a75;
    text-align: center;
}

.stButton>button {
    background-color: #ff66b3;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

.stSlider>div>div>div>div {
    color: #ff1a75;
}

.result-card {
    background-color: #ffe6f0;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    border: 2px solid #ff66b3;
    box-shadow: 2px 2px 10px rgba(255,102,179,0.3);
}
a {
    color: #ff1a75;
    text-decoration: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.title("🌸 Multi-Site Search Tool")
st.write("Search across TikTok, YouTube, Reddit, Twitter, and   Wikipedia!")

# Text input for query
query = st.text_input("🔎 Enter your search query:")

# Slider for number of results
num_results = st.slider("Select number of results", min_value=1, max_value=20, value=5)

# Checkbox-based site selection
st.write("Select websites to search in:")
col1, col2 = st.columns(2)

with col1:
    tiktok = st.checkbox("TikTok", value=True)
    youtube = st.checkbox("YouTube", value=True)
    reddit = st.checkbox("Reddit")
with col2:
    twitter = st.checkbox("Twitter")
    stackoverflow = st.checkbox("Wikipedia")

# Create domain list based on selection
include_domains = []
if tiktok: include_domains.append("https://www.tiktok.com")
if youtube: include_domains.append("https://www.youtube.com")
if reddit: include_domains.append("https://www.reddit.com")
if twitter: include_domains.append("https://twitter.com")
if stackoverflow: include_domains.append("https://en.wikipedia.org")

# Button to trigger search
if st.button("🚀 Search"):
    if not query:
        st.warning("⚠️ Please enter a search query first.")
    elif not include_domains:
        st.warning("⚠️ Please select at least one site.")
    else:
        st.info("🔍 Searching... Please wait.")
        try:
            # Perform the Exa search
            response = exa.search(
                query=query,
                num_results=num_results,
                type="keyword",
                include_domains=include_domains
            )

            # Display results
            if response.results:
                st.success(f"✅ Found {len(response.results)} results!")
                for result in response.results:
                    st.markdown(f"""
                    <div class="result-card">
                        📄 <a href="{result.url}" target="_blank">{result.title}</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("❌ No results found. Try a different query.")
        except Exception as e:
            st.error(f"🚨 Error: {e}")


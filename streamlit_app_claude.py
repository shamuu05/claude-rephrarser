# streamlit_app_claude.py

import streamlit as st
import os
from main_claude import rephrase_full_transcript

st.set_page_config(page_title="Claude Transcript Rewriter (Full)", layout="wide")
st.title("📄 Full Transcript Rewriter with Claude API")

# Claude API Key Input
claude_key = st.text_input("🔑 Claude API Key:", type="password")

# Tone Selection
tone = st.selectbox("🎨 Choose Tone", [
    "Neutral", "Formal", "Casual", "Humorous", "Motivational", 
    "Empathetic", "Assertive", "Professional", "Poetic", "Excited"
])

# Style Selection
style = st.selectbox("✍️ Choose Style", [
    "Default", "Meme-style", "Storytelling", "Inspirational", "Socratic",
    "Bullet points", "Explanatory", "Twitter-thread", "Narrative", "Educational"
])

# Additional Controls
preserve_story = st.checkbox("📚 Keep storytelling format/style")
length_multiplier = st.slider("📏 Rephrased length multiplier", 0.5, 2.0, 1.0, 0.1)

# Transcript Input
input_text = st.text_area("📝 Paste your full transcript (max ~10,000 tokens):", height=300)

# Buttons
start_button = st.button("🚀 Start Rephrasing")
stop_button = st.button("🛑 Stop")

# Process
if claude_key:
    os.environ["CLAUDE_API_KEY"] = claude_key

    if start_button:
        if not input_text.strip():
            st.warning("Please paste your transcript first.")
        else:
            with st.spinner("Rephrasing entire transcript with Claude..."):
                final_output = rephrase_full_transcript(
                    transcript=input_text,
                    tone=tone,
                    style=style,
                    storytelling=preserve_story,
                    length_multiplier=length_multiplier
                )

            st.subheader("📝 Rephrased Transcript")
            st.text_area("Final Output:", value=final_output, height=500)
            st.download_button("📥 Download", data=final_output, file_name="claude_full_rephrased_transcript.txt")

    if stop_button:
        st.warning("⛔ Process manually stopped.")
else:
    st.info("Please enter your Claude API key.")

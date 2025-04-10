# streamlit_app_claude.py

import streamlit as st
import os
from main_claude import rephrase_full_transcript

st.set_page_config(page_title="Claude Transcript Rewriter", layout="wide")
st.title("📄 Claude-3 Transcript Rewriter")

# Claude API key input
claude_key = st.text_input("🔑 Claude API Key:", type="password")

# User controls
tone = st.selectbox("🎨 Choose Tone", [
    "Neutral", "Formal", "Casual", "Humorous", "Motivational", 
    "Empathetic", "Assertive", "Professional", "Poetic", "Excited"
])

style = st.selectbox("✍️ Choose Style", [
    "Default", "Meme-style", "Storytelling", "Inspirational", "Socratic",
    "Bullet points", "Explanatory", "Twitter-thread", "Narrative", "Educational"
])

preserve_story = st.checkbox("📚 Keep storytelling format/style")
length_multiplier = st.slider("📏 Rephrased length multiplier", 0.5, 2.0, 1.0, 0.1)

input_text = st.text_area("📝 Paste your full transcript here (up to ~10k tokens):", height=300)

start_button = st.button("🚀 Start Rephrasing")
stop_button = st.button("🛑 Stop")

if claude_key:
    os.environ["CLAUDE_API_KEY"] = claude_key

    if start_button:
        if not input_text.strip():
            st.warning("Please paste your transcript.")
        else:
            with st.spinner("Rephrasing the full transcript with Claude..."):
                try:
                    final_output = rephrase_full_transcript(
                        transcript=input_text,
                        tone=tone,
                        style=style,
                        storytelling=preserve_story,
                        length_multiplier=length_multiplier
                    )
                    st.success("✅ Rephrasing complete!")
                    st.subheader("📝 Rephrased Transcript")
                    st.text_area("Final Output", value=final_output, height=500)
                    st.download_button("📥 Download", data=final_output, file_name="claude_rephrased_transcript.txt")
                except Exception as e:
                    st.error(f"⚠️ Error while contacting Claude API:\n{e}")

    if stop_button:
        st.warning("⛔ You stopped the process.")
else:
    st.info("Please enter your Claude API key to begin.")

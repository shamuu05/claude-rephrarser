# streamlit_app_claude.py

import streamlit as st
from main_claude import rephrase_full_transcript

st.set_page_config(page_title="Claude Transcript Rewriter", layout="wide")
st.title("📄 Claude-3 Transcript Rewriter")

# Claude API Key
claude_key = st.text_input("🔑 Claude API Key", type="password")

# Claude Model Selector
model = st.selectbox("🤖 Select Claude Model", [
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229"
])

# User Customizations
tone = st.selectbox("🎨 Choose Tone", [
    "Neutral", "Formal", "Casual", "Humorous", "Motivational", 
    "Empathetic", "Assertive", "Professional", "Poetic", "Excited"
])

style = st.selectbox("✍️ Choose Script Style", [
    "Default", "Meme-style", "Storytelling", "Inspirational", "Socratic",
    "Bullet points", "Explanatory", "Twitter-thread", "Narrative", "Educational"
])

preserve_story = st.checkbox("📚 Keep storytelling format/style")
length_multiplier = st.slider("📏 Rephrased Length Multiplier", 0.5, 2.0, 1.0, 0.1)

# Transcript Input
input_text = st.text_area("📝 Paste your full transcript:", height=300)

# Buttons
start_button = st.button("🚀 Start Rephrasing")
stop_button = st.button("🛑 Stop")

if claude_key:
    if start_button:
        if not input_text.strip():
            st.warning("Please paste a transcript.")
        else:
            with st.spinner("Rephrasing entire transcript with Claude..."):
                try:
                    final_output = rephrase_full_transcript(
                        transcript=input_text,
                        api_key=claude_key,
                        model=model,
                        tone=tone,
                        style=style,
                        storytelling=preserve_story,
                        length_multiplier=length_multiplier
                    )

                    st.success("✅ Rephrasing complete!")
                    st.subheader("📝 Rephrased Transcript")
                    st.text_area("Result", value=final_output, height=500)
                    st.download_button("📥 Download", data=final_output, file_name="claude_rephrased.txt")

                except Exception as e:
                    st.error(f"❌ Error from Claude API: {e}")

    if stop_button:
        st.warning("⛔ You stopped the rephrasing process.")
else:
    st.info("Please enter your Claude API key to begin.")

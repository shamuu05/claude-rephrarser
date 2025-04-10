import streamlit as st
import os
from main_claude import split_transcript, rephrase_each_paragraph, combine_rephrased_text

st.set_page_config(page_title="Claude Transcript Rewriter", layout="wide")
st.title("📄 Transcript Rewriter with Claude API")

claude_key = st.text_input("🔑 Claude API Key:", type="password")

tone = st.selectbox("🎨 Choose Tone (optional)", [
    "Default", "Formal", "Casual", "Humorous", "Motivational", 
    "Empathetic", "Assertive", "Professional", "Poetic", "Neutral"
])

style = st.selectbox("✍️ Choose Script Style (optional)", [
    "Default", "Meme-style", "Storytelling", "Inspirational", "Socratic",
    "Bullet points", "Explanatory", "Twitter-thread", "Narrative", "Educational"
])

preserve_story = st.checkbox("📚 Keep storytelling format/style")

para_len = st.slider("🧱 Paragraph word count", 50, 500, 200, 50)
extend_limit = st.slider("📏 Rephrasing length multiplier", 0.5, 2.0, 1.0, 0.1)

input_text = st.text_area("📝 Paste your transcript here:", height=300)

start_button = st.button("🚀 Start Rephrasing")
stop_button = st.button("🛑 Stop")

if claude_key:
    os.environ["CLAUDE_API_KEY"] = claude_key

    if start_button:
        if not input_text.strip():
            st.warning("Please paste a transcript.")
        else:
            st.success("Starting...")

            with st.spinner("Splitting into paragraphs..."):
                paragraphs = split_transcript(input_text, max_words_per_paragraph=para_len)

            instruction = f"Write in a {tone} tone, using {style} style."
            if preserve_story:
                instruction += " Preserve the storytelling structure."
            instruction += f" Expand or shorten as needed to match a {extend_limit:.1f}x length."

            with st.spinner("Rephrasing with Claude..."):
                rephrased = rephrase_each_paragraph(paragraphs, instruction=instruction)

            final_output = combine_rephrased_text(rephrased)

            st.subheader("📝 Rephrased Transcript")
            st.text_area("Final Output:", value=final_output, height=500)
            st.download_button("📥 Download", data=final_output, file_name="claude_rephrased_transcript.txt")

    if stop_button:
        st.warning("⛔ Process manually stopped.")
else:
    st.info("Please enter your Claude API key.")
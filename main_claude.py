import anthropic
import os
import re

# Setup Claude Client
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def call_claude(prompt):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def split_transcript(text, max_words_per_paragraph=200):
    words = text.split()
    paragraphs = []
    for i in range(0, len(words), max_words_per_paragraph):
        chunk = " ".join(words[i:i+max_words_per_paragraph])
        paragraphs.append(chunk)
    return paragraphs

def rephrase_each_paragraph(paragraphs, instruction=None):
    rephrased = []
    for i, para in enumerate(paragraphs):
        prompt = f"{instruction}\n\nPlease rephrase the following paragraph while preserving its meaning:\n\n{para}"
        try:
            response = call_claude(prompt)
            rephrased.append(response)
        except Exception as e:
            rephrased.append(f"[Error rephrasing paragraph {i+1}: {e}]")
    return rephrased

def combine_rephrased_text(paragraphs):
    return "\n\n".join(paragraphs)
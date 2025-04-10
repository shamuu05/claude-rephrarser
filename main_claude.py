# main_claude.py

import anthropic
import os

# Setup Claude Client
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def rephrase_full_transcript(transcript, tone="neutral", style="default", storytelling=False, length_multiplier=1.0):
    instructions = f"Rephrase the following transcript in a {tone} tone using {style} style."
    if storytelling:
        instructions += " Maintain the storytelling structure."
    instructions += f" Keep the rephrased text roughly the same length as the original (about {length_multiplier:.1f}x the original length)."

    prompt = f"{instructions}\n\nTranscript:\n{transcript}"

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

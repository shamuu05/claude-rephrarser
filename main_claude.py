# main_claude.py

import anthropic
import os

# Initialize Claude client with environment variable
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def rephrase_full_transcript(transcript, tone="neutral", style="default", storytelling=False, length_multiplier=1.0):
    # Build instructions
    instructions = f"Rephrase the following transcript in a {tone} tone using {style} style."
    if storytelling:
        instructions += " Maintain the storytelling structure."
    instructions += f" Make the rephrased text approximately {length_multiplier:.1f} times the original length."

    full_prompt = f"{instructions}\n\nTranscript:\n{transcript}"

    # Claude-3 API expects messages as a list of dicts with 'type: text'
    response = client.messages.create(
        model="claude-3-sonnet-20240229",  # You can also try "claude-3-haiku-20240307"
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": full_prompt
                    }
                ]
            }
        ]
    )

    # Return the response text
    return response.content[0].text.strip()

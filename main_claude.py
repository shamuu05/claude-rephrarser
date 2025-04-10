# main_claude.py

import anthropic

def rephrase_full_transcript(transcript, api_key, model="claude-3-sonnet-20240229",
                             tone="neutral", style="default", storytelling=False, length_multiplier=1.0):
    # Init client with explicit key
    client = anthropic.Anthropic(api_key=api_key)

    # Build prompt instructions
    instructions = f"Rephrase the following transcript in a {tone} tone using {style} style."
    if storytelling:
        instructions += " Maintain the storytelling structure."
    instructions += f" Make the rephrased text approximately {length_multiplier:.1f} times the original length."

    full_prompt = f"{instructions}\n\nTranscript:\n{transcript}"

    # Make Claude API call
    response = client.messages.create(
        model=model,
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

    return response.content[0].text.strip()

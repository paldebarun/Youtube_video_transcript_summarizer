def summarization_prompt(transcript: str) -> str:
    return f"""
You are an expert AI assistant.

Summarize the following YouTube transcript.

Return ONLY valid JSON.

Format:

{{
    "title": "...",
    "summary": "...",
    "key_points": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ]
}}

Transcript:

{transcript}
"""
import json


def summarization_prompt(
    transcript: str,
    ocr: dict,
    metadata: dict,
) -> str:

    return f"""
You are an expert AI assistant specialized in understanding YouTube videos.

You have three information sources:

1. Spoken transcript.
2. Text detected from video frames (OCR).
3. Video metadata.

Your task is to combine ALL of these sources into one coherent summary.

Rules:

- Use the transcript as the primary source.
- Use OCR to enrich the summary with:
    - slide titles
    - code snippets
    - chapter headings
    - diagrams
    - equations
    - UI labels
    - text shown on screen
- Use metadata only for context.
- Ignore OCR text that is obviously noisy or unrelated.
- Never invent facts that are not present.
- Return ONLY valid JSON.

Video Metadata

{json.dumps(metadata, indent=2)}

Detected On-Screen Text

{json.dumps(ocr, indent=2)}

Transcript

{transcript}

Return EXACTLY this JSON:

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
"""
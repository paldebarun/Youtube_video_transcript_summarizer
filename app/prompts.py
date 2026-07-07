import json


def summarization_prompt(
    transcript: str,
    ocr: dict,
    metadata: dict,
    vision: dict,
) -> str:

    return f"""
You are an expert AI assistant specialized in understanding YouTube videos.

You have four information sources:

1. Spoken transcript.
2. Text detected from video frames (OCR).
3. Vision analysis of the video frames.
4. Video metadata.

Your task is to combine ALL of these sources into one coherent summary.

Rules:

- Use the transcript as the primary source.
- Use OCR to enrich the summary with:
    - slide titles
    - code snippets
    - chapter headings
    - equations
    - UI labels
    - text shown on screen.
- Use the vision analysis to understand:
    - scenes
    - objects
    - people
    - activities
    - charts
    - diagrams
    - visual context
    - UI layouts
    - anything important visible in the frames.
- Use metadata only as supporting context.
- Ignore OCR or Vision results that are noisy or irrelevant.
- Never invent facts that are not present.
- Combine information from transcript, OCR and Vision whenever possible.
- Return ONLY valid JSON.

Video Metadata

{json.dumps(metadata, indent=2)}

Vision Analysis

{json.dumps(vision, indent=2)}

Detected On-Screen Text (OCR)

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
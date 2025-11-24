import json
import re

def safe_extract_json(text):
    """
    Extract the first JSON object found in LLM output.
    Handles extra text, broken formatting, and UTF-8 characters.
    """
    text = text.encode("utf-8", "ignore").decode("utf-8")

    # Try direct JSON first
    try:
        return json.loads(text)
    except:
        pass

    # Extract JSON substring using regex
    json_blocks = re.findall(r"\{.*?\}", text, re.DOTALL)
    if not json_blocks:
        return {"english": "", "finnish": "", "state": ""}

    try:
        return json.loads(json_blocks[0])
    except:
        return {"english": "", "finnish": "", "state": ""}


def parse_ai_response(ai_response_text):
    """
    Extracts english, finnish, and state fields from LLM JSON output.
    Ensures UTF-8 characters (ä, ö, å) remain intact.
    """
    result = safe_extract_json(ai_response_text)

    english = result.get("english", "")
    finnish = result.get("finnish", "")
    state = result.get("state", "")

    return {
        "english": english,
        "finnish": finnish,
        "state": state
    }

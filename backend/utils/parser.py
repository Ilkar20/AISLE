import json
import re

def safe_extract_json(text):
    """
    Extract the first JSON object found in LLM output.
    Handles extra text, broken formatting, and UTF-8 characters.
    """
    text = text.encode("utf-8", "ignore").decode("utf-8")

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

    # If the parser couldn't extract any of the expected fields,
    # fall back to returning the raw LLM output so the frontend can
    # display something useful to the user instead of empty strings.
    if not (english or finnish or state):
        # Prefer a trimmed raw text (preserve utf-8)
        raw_text = ai_response_text.encode("utf-8", "ignore").decode("utf-8").strip()
        # Put the raw text into `english` so existing UI shows it.
        return {
            "english": raw_text,
            "finnish": "",
            "state": "",
            "raw": raw_text,
        }

    return {
        "english": english,
        "finnish": finnish,
        "state": state,
        "raw": result,
    }

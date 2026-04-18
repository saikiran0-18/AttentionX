import re


IMPORTANT_WORDS = {
    "important", "powerful", "secret", "best", "mistake", "growth",
    "success", "failure", "lesson", "hack", "strategy", "framework",
    "career", "interview", "placement", "resume", "job", "money",
    "viral", "attention", "content", "audience", "creator", "mentor",
    "students", "problem", "solution", "build", "startup"
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def score_segment(text: str) -> float:
    text = clean_text(text)
    lower = text.lower()

    score = 0.0

    word_count = len(lower.split())
    score += min(word_count / 10, 4)

    score += lower.count("!") * 1.2
    score += lower.count("?") * 0.8

    words = set(re.findall(r"\b[a-zA-Z]+\b", lower))
    hits = len(words.intersection(IMPORTANT_WORDS))
    score += hits * 1.5

    if "you should" in lower:
        score += 1.5
    if "don't" in lower or "do not" in lower:
        score += 1.0
    if "how to" in lower:
        score += 1.3

    return score


def merge_nearby_segments(segments: list, gap_threshold: float = 2.0) -> list:
    if not segments:
        return []

    merged = [segments[0].copy()]

    for seg in segments[1:]:
        last = merged[-1]
        if seg["start"] - last["end"] <= gap_threshold:
            last["end"] = seg["end"]
            last["text"] += " " + seg["text"]
        else:
            merged.append(seg.copy())

    return merged


def find_top_highlights(segments: list, top_k: int = 3, min_len: float = 15, max_len: float = 45) -> list:
    merged = merge_nearby_segments(segments)
    candidates = []

    for seg in merged:
        duration = seg["end"] - seg["start"]
        if duration < min_len:
            continue

        start = seg["start"]
        end = min(seg["end"], seg["start"] + max_len)
        text = clean_text(seg["text"])
        score = score_segment(text)

        candidates.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "text": text,
            "score": round(score, 2)
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)

    selected = []
    for cand in candidates:
        overlap = False
        for picked in selected:
            if not (cand["end"] < picked["start"] or cand["start"] > picked["end"]):
                overlap = True
                break

        if not overlap:
            selected.append(cand)

        if len(selected) == top_k:
            break

    return selected